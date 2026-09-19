"""Allowlisted SQLite query over local fictional exposure events."""

import sqlite3
from .models import InputError


EXPOSURE_SQL = """SELECT COALESCE(SUM(violation), 0) AS numerator, COUNT(*) AS denominator
FROM exposure
WHERE build = ? AND platform = ? AND config = ? AND metric = ?
  AND eligible = 1 AND second >= 0 AND second < ?"""


def query_exposure(bundle, metric):
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE exposure (build TEXT, platform TEXT, config TEXT, metric TEXT, event_id TEXT, eligible INTEGER, violation INTEGER, second INTEGER, PRIMARY KEY(build, platform, config, metric, event_id))")
        for row in bundle.select("metric_event"):
            d = row["data"]
            if any(key not in d for key in ("config", "metric", "event_id", "eligible", "violation", "second")):
                raise InputError("Exposure event is missing a required field.")
            if type(d["eligible"]) is not bool or type(d["violation"]) is not bool or type(d["second"]) is not int:
                raise InputError("Exposure flags must be booleans and event seconds integers.")
            values = (row["build"], row["platform"], d["config"], d["metric"], d["event_id"], int(d["eligible"]), int(d["violation"]), d["second"])
            old = connection.execute("SELECT * FROM exposure WHERE build=? AND platform=? AND config=? AND metric=? AND event_id=?", values[:5]).fetchone()
            if old and old != values:
                raise InputError("Duplicate event identity has conflicting contents.")
            connection.execute("INSERT OR IGNORE INTO exposure VALUES (?,?,?,?,?,?,?,?)", values)
        d = metric["data"]
        parameters = (metric["build"], metric["platform"], d["config"], d["metric"], d["window_seconds"])
        numerator, denominator = connection.execute(EXPOSURE_SQL, parameters).fetchone()
        return {"sql": EXPOSURE_SQL, "parameters": list(parameters), "numerator": numerator, "denominator": denominator}
    finally:
        connection.close()
