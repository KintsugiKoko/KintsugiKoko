"""Optional explicit network adapter; offline use never imports credentials."""

import json
import os
import urllib.error
import urllib.request
from .models import InputError


def action_schema(allowed):
    return {"type": "object", "additionalProperties": False, "required": ["tool", "argument", "notes"], "properties": {
        "tool": {"type": "string", "enum": allowed}, "argument": {"type": "string"},
        "notes": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["text", "kind", "evidence"], "properties": {"text": {"type": "string"},
            "kind": {"type": "string", "enum": ["hypothesis", "next_action"]},
            "evidence": {"type": "array", "items": {"type": "string"}}}}}}}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InputError("Model endpoint redirect rejected.")


class OpenAIPolicy:
    """Structured action selection over a fixed local tool set."""

    name = "model_tool_loop"

    def __init__(self, *, enabled=False, model=None, transport=None):
        if not enabled:
            raise InputError("Network mode requires --allow-network.")
        self.model = model or os.environ.get("OPENAI_MODEL", "")
        self._key = os.environ.get("OPENAI_API_KEY", "")
        if not self.model or not self._key:
            raise InputError("Set OPENAI_MODEL and OPENAI_API_KEY in the environment for model mode.")
        self._transport = transport or urllib.request.build_opener(NoRedirect()).open
        self.usage = {"input_tokens": 0, "output_tokens": 0, "requests": 0}

    def choose(self, context):
        evidence_context = {k: v for k, v in context.items() if k != "instructions"}
        payload = {"model": self.model, "store": False, "max_output_tokens": 1600,
                   "input": [{"role": "developer", "content": context["instructions"]},
                             {"role": "user", "content": json.dumps(evidence_context)}],
                   "text": {"format": {"type": "json_schema", "name": "qa_action", "strict": True,
                                        "schema": action_schema(context["allowed_tools"])}}}
        encoded = json.dumps(payload).encode()
        if len(encoded) > 200_000:
            raise InputError("Model context exceeds the 200 KB request budget.")
        request = urllib.request.Request("https://api.openai.com/v1/responses", data=encoded,
            headers={"Content-Type": "application/json", "Authorization": "Bearer " + self._key}, method="POST")
        try:
            with self._transport(request, timeout=min(30, context["remaining_seconds"])) as response:
                raw = response.read(1_000_001)
                if len(raw) > 1_000_000:
                    raise InputError("Model response exceeds the response budget.")
                data = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeError, OSError):
            # Server bodies and exception reprs may contain submitted text or headers.
            raise InputError("Model request failed; no automatic retry. Review connectivity and account access.") from None
        self.usage["requests"] += 1
        if not isinstance(data, dict):
            raise InputError("Model response must be a structured object.")
        usage = data.get("usage", {})
        if not isinstance(usage, dict) or any(type(usage.get(key, 0)) is not int or usage.get(key, 0) < 0
                                            for key in ("input_tokens", "output_tokens")):
            raise InputError("Model response contains invalid token accounting.")
        for key in ("input_tokens", "output_tokens"):
            self.usage[key] += usage.get(key, 0)
        if data.get("status") != "completed":
            raise InputError("Model response did not complete; preserve the blocked run.")
        output = data.get("output")
        if not isinstance(output, list):
            raise InputError("Model response output must be a list.")
        texts = []
        for item in output:
            if not isinstance(item, dict):
                raise InputError("Model response contains an invalid output item.")
            if item.get("type") != "message":
                continue
            content = item.get("content")
            if not isinstance(content, list):
                raise InputError("Model message content must be a list.")
            for part in content:
                if not isinstance(part, dict):
                    raise InputError("Model response contains invalid message content.")
                if part.get("type") == "output_text":
                    if not isinstance(part.get("text"), str):
                        raise InputError("Model action text must be a string.")
                    texts.append(part["text"])
        if len(texts) != 1:
            raise InputError("Model returned no single structured action.")
        try:
            return json.loads(texts[0])
        except json.JSONDecodeError:
            raise InputError("Model action was not valid JSON.") from None
