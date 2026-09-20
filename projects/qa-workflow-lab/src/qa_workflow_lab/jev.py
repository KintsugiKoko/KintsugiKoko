"""Optional TypeSafe transport. Disabled until explicitly enabled by the caller."""

import json
import os
import re
import time
import urllib.error
import urllib.request

from .models import InputError
from .provider import NoRedirect
from .routing import request_payload, validate_answer


ENDPOINT = "https://api.typesafe.ai/v1/systemone"


class JevRouter:
    def __init__(self, *, enabled=False, model="jev-latest", max_calls=20, transport=None):
        if not enabled:
            raise InputError("Jev mode requires --allow-network; it sends fictional reports to TypeSafe.")
        if not re.fullmatch(r"jev-[A-Za-z0-9_.-]{1,60}", model):
            raise InputError("Use a Jev model ID, not a URL or secret.")
        if type(max_calls) is not int or not 1 <= max_calls <= 20:
            raise InputError("Jev request cap must be between 1 and 20.")
        self._key = os.environ.get("TYPESAFE_API_KEY", "")
        if not self._key or any(char.isspace() for char in self._key):
            raise InputError("Set TYPESAFE_API_KEY through the local environment, never in a file or report.")
        self.model, self.max_calls = model, max_calls
        self._transport = transport or urllib.request.build_opener(NoRedirect()).open
        self.deadline = time.monotonic() + 60
        self.usage = {"attempts": 0, "responses": 0, "input_tokens": 0, "output_tokens": 0}
        self.trace = []
        self.stopped = False

    def choose(self, report):
        remaining = self.deadline - time.monotonic()
        if self.stopped or self.usage["attempts"] >= self.max_calls or remaining <= 0:
            raise InputError("Jev request budget exhausted or circuit stopped; human review required.")
        encoded = json.dumps(request_payload(report, self.model)).encode("utf-8")
        if len(encoded) > 20_000:
            raise InputError("Jev request exceeds the 20 KB request budget.")
        request = urllib.request.Request(ENDPOINT, data=encoded, method="POST", headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self._key})
        started = time.monotonic()
        self.usage["attempts"] += 1
        try:
            with self._transport(request, timeout=min(10, remaining)) as response:
                raw = response.read(64_001)
            if len(raw) > 64_000:
                raise InputError("Jev response exceeds the 64 KB response budget.")
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise InputError("Invalid Jev response envelope.")
            model = data.get("model")
            if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9_.:/-]{1,80}", model):
                raise InputError("Invalid Jev response model identity.")
            usage = data.get("usage")
            if not isinstance(usage, dict) or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("input_tokens", "output_tokens")):
                raise InputError("Invalid Jev token accounting.")
            answers = data.get("answers")
            if not isinstance(answers, dict) or set(answers) != {"route"}:
                raise InputError("Jev must return exactly one routing answer.")
            answer = answers["route"]
            validate_answer(answer)
        except (InputError, urllib.error.URLError, TimeoutError, OSError, ValueError, UnicodeError):
            # Never persist server bodies, exception messages, submitted headers or keys.
            self.stopped = True
            self.trace.append({"id": report["id"], "status": "stopped", "elapsed_ms": round((time.monotonic() - started) * 1000, 2)})
            raise InputError("Jev request or response failed; circuit stopped, no retry. Review account or contract locally.") from None
        self.usage["responses"] += 1
        for key in ("input_tokens", "output_tokens"):
            self.usage[key] += usage[key]
        self.trace.append({"id": report["id"], "status": "response_valid", "model": model,
                           "elapsed_ms": round((time.monotonic() - started) * 1000, 2)})
        return answer
