#!/usr/bin/env python3
"""Generate /.well-known/x402-service.json from the LIVE paidgate offer.

The payment fields are never typed twice: this imports /opt/data/serve/paidgate.py
and calls offer(), so the published discovery manifest cannot drift from the
terms the server actually enforces. true402's gate is one JSON manifest in the
served directory; this is that artifact, not a settlement and not revenue.
"""
import importlib.util
import json
import os

PAIDGATE = "/opt/data/serve/paidgate.py"
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "x402-service.json")
SERVE_OUT = "/opt/data/serve/x402-service.json"
HOST = "seed-0x01.konnektr.io"


def load_paidgate():
    spec = importlib.util.spec_from_file_location("paidgate_live_x402svc", PAIDGATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(host=HOST):
    """Return the manifest object, bound field-for-field to offer()."""
    offer = load_paidgate().offer(host)
    acc = offer["accepts"][0]
    res = offer["resource"]
    return {
        "x402Version": offer["x402Version"],
        "service": {
            "name": res["serviceName"],
            "provider": "Tallow (autonomous AI agent, not a human)",
            "homepage": "https://%s/" % host,
        },
        "resources": [
            {
                "url": res["url"],
                "method": "GET",
                "description": res["description"],
                "mimeType": res["mimeType"],
                "scheme": acc["scheme"],
                "network": acc["network"],
                "asset": acc["asset"],
                "amount": acc["amount"],
                "payTo": acc["payTo"],
                "maxTimeoutSeconds": acc["maxTimeoutSeconds"],
                "extra": acc["extra"],
                "extensions": offer["extensions"],
            }
        ],
    }


def render(host=HOST):
    """Deterministic bytes: no clock, no host state, stable sha256."""
    return (json.dumps(build(host), indent=2, sort_keys=True,
                             ensure_ascii=True) + "\n").encode("utf-8")


def write(host=HOST):
    data = render(host)
    with open(SOURCE, "wb") as f:
        f.write(data)
    with open(SERVE_OUT, "wb") as f:
        f.write(data)
    return data


if __name__ == "__main__":
    d = write()
    print("wrote %s + %s (%d bytes)" % (SOURCE, SERVE_OUT, len(d)))
