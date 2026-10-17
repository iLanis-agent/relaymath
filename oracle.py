#!/usr/bin/env python3
# Relay Math oracle - mirrors engine.js.
import json, math, re

KM_PER_MILE = 1.609344

def _pos(x, msg):
    if not math.isfinite(x) or x <= 0:
        raise ValueError(msg)

def _nonneg(x, msg):
    if not math.isfinite(x) or x < 0:
        raise ValueError(msg)

def _clock(s):
    h, rem = divmod(s, 3600)
    m, r = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{r:02d}"
    return f"{m}:{r:02d}"

def _km(x):
    return str(int(x)) if x == int(x) else repr(x)

def pace_truth(distance_km, minutes, seconds):
    _pos(distance_km, "distance must be more than 0 km")
    _nonneg(minutes, "minutes must be 0 or more")
    _nonneg(seconds, "seconds must be 0 or more")
    total = math.floor(minutes * 60 + seconds + 0.5)
    if total <= 0:
        raise ValueError("enter a finish time over 0")
    per_km = math.floor(total / distance_km + 0.5)
    per_mile = math.floor(total / (distance_km / KM_PER_MILE) + 0.5)
    return f"{_km(distance_km)} km in {_clock(total)} is {_clock(per_km)} per km, {_clock(per_mile)} per mile."

def finish_truth(distance_km, pace_min, pace_sec):
    _pos(distance_km, "distance must be more than 0 km")
    _nonneg(pace_min, "minutes must be 0 or more")
    _nonneg(pace_sec, "seconds must be 0 or more")
    pace = math.floor(pace_min * 60 + pace_sec + 0.5)
    if pace <= 0:
        raise ValueError("enter a pace over 0")
    total = math.floor(pace * distance_km + 0.5)
    return f"A {_clock(pace)} per km pace over {_km(distance_km)} km finishes in {_clock(total)}."

def relay_truth(legs):
    if len(legs) < 2:
        raise ValueError("a relay needs at least 2 legs")
    secs = []
    for i, x in enumerate(legs):
        m = re.match(r"^(\d{1,3}):([0-5]\d)$", str(x).strip())
        if not m:
            raise ValueError(f"leg {i + 1} must look like 12:10")
        s = int(m.group(1)) * 60 + int(m.group(2))
        if s == 0:
            raise ValueError(f"leg {i + 1} must be over 0:00")
        secs.append(s)
    total, lo, hi = sum(secs), min(secs), max(secs)
    head = f"{len(secs)} legs: " + " + ".join(_clock(s) for s in secs) + f" = {_clock(total)}"
    if hi == lo:
        return head + " - every leg the same."
    return head + f" - slowest {_clock(hi)}, fastest {_clock(lo)}, a gap of {_clock(hi - lo)}."

CASES = [
    ("paceTruth", (10, 52, 30)),
    ("paceTruth", (21.0975, 105, 0)),
    ("paceTruth", (5, 0, 59)),
    ("paceTruth", (42.195, 240, 0)),
    ("paceTruth", (0, 50, 0)),
    ("paceTruth", (10, 0, 0)),
    ("finishTruth", (10, 5, 15)),
    ("finishTruth", (5, 4, 30)),
    ("finishTruth", (42.195, 5, 40)),
    ("finishTruth", (10, 0, 0)),
    ("relayTruth", (["12:10", "11:45", "13:02", "12:30"],)),
    ("relayTruth", (["10:00", "10:00"],)),
    ("relayTruth", (["59:59", "1:01", "20:00"],)),
    ("relayTruth", (["12:10"],)),
    ("relayTruth", (["12:10", "1210", "13:02", "12:30"],)),
    ("relayTruth", (["12:10", "0:00", "13:02", "12:30"],)),
]
FNS = {"paceTruth": pace_truth, "finishTruth": finish_truth, "relayTruth": relay_truth}
out = []
for name, args in CASES:
    try:
        e = FNS[name](*args)
    except ValueError as ex:
        e = "ERR:" + str(ex)
    out.append({"fn": name, "args": list(args), "expected": e})
with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
