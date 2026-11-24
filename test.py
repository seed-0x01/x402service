#!/usr/bin/env python3
"""Fixtures: the manifest must be the live offer, and the served copy exact."""
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("x402svc_build", os.path.join(HERE, "build.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


offer = b.load_paidgate().offer(b.HOST)
acc = offer["accepts"][0]
res = offer["resource"]

with open(b.SOURCE, "rb") as f:
    source_bytes = f.read()
doc = json.loads(source_bytes)          # valid JSON, or the test dies here
r = doc["resources"][0]

check("x402Version == offer", doc["x402Version"] == offer["x402Version"])
check("url == live resource url", r["url"] == res["url"])
check("scheme is exact", r["scheme"] == "exact" and r["scheme"] == acc["scheme"])
check("network eip155:8453", r["network"] == "eip155:8453" and r["network"] == acc["network"])
check("amount bound to offer", r["amount"] == acc["amount"] == "50000")
check("asset bound to offer", r["asset"] == acc["asset"])
check("payTo bound to offer", r["payTo"] == acc["payTo"])
check("extensions bound to offer", r["extensions"] == offer["extensions"])
check("deterministic render", b.render() == source_bytes)
check("served copy byte-exact", open(b.SERVE_OUT, "rb").read() == source_bytes)
check("no settlement/revenue claim fields", not any(
    w in doc or w in r for w in
    ("settled_payments", "outside_payers", "revenue", "settlement", "earned")))

passed = sum(1 for _, ok in checks if ok)
for name, ok in checks:
    print(("PASS " if ok else "FAIL ") + name)
print("%d/%d PASS" % (passed, len(checks)))
print("sha256 %s" % hashlib.sha256(source_bytes).hexdigest())
sys.exit(0 if passed == len(checks) else 1)
