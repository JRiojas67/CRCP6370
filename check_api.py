#!/usr/bin/env python3
"""
Verify that all chatbot APIs are correctly implemented.
Run with the server already running: python3 server.py (in another terminal).
Then run: python3 check_api.py
"""

import urllib.request
import urllib.error
import json
import sys

BASE = "http://127.0.0.1:5500"
errors = []


def req(path, method="GET", data=None):
    url = BASE + path
    headers = {}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.getcode(), r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode() if e.fp else ""
    except urllib.error.URLError as e:
        return None, "Connection refused (is the server running? python3 server.py)"
    except Exception as e:
        return None, str(e)


def check(name, code, expected_code, body_contains=None, body=None):
    if code is None:
        errors.append("%s: %s" % (name, body_contains or "connection failed"))
        return False
    if code != expected_code:
        errors.append("%s: expected HTTP %s, got %s" % (name, expected_code, code))
        return False
    if body_contains and body_contains not in (body or ""):
        errors.append("%s: response missing %r" % (name, body_contains))
        return False
    return True


def main():
    print("Checking APIs at %s (start server with: python3 server.py)\n" % BASE)

    # GET /
    code, body = req("/")
    if check("GET /", code, 200, "<title>", body):
        print("  GET /                 OK (200)")
    else:
        print("  GET /                 FAIL")

    # GET /api/health
    code, body = req("/api/health")
    ok = check("GET /api/health", code, 200, '"ok": true', body)
    if ok:
        try:
            d = json.loads(body)
            if d.get("ok") and "message" in d:
                print("  GET /api/health        OK (200) ok=true")
            else:
                errors.append("GET /api/health: response should have ok and message")
                print("  GET /api/health        FAIL (wrong shape)")
        except json.JSONDecodeError:
            errors.append("GET /api/health: invalid JSON")
            print("  GET /api/health        FAIL (invalid JSON)")
    else:
        print("  GET /api/health        FAIL")

    # OPTIONS /api/chat
    code, _ = req("/api/chat", method="OPTIONS")
    if check("OPTIONS /api/chat", code, 204):
        print("  OPTIONS /api/chat      OK (204)")
    else:
        print("  OPTIONS /api/chat      FAIL")

    # POST /api/chat (empty message -> 400)
    code, body = req("/api/chat", method="POST", data={"message": "", "personality": "default"})
    if check("POST /api/chat (empty)", code, 400, "error", body):
        print("  POST /api/chat empty   OK (400)")
    else:
        print("  POST /api/chat empty   FAIL")

    # POST /api/chat (valid) - may 200 or 503 if no API keys
    code, body = req("/api/chat", method="POST", data={"message": "Hello", "personality": "default"})
    if code == 200:
        try:
            d = json.loads(body)
            if "response" in d:
                print("  POST /api/chat         OK (200) has response")
            else:
                errors.append("POST /api/chat: 200 response should contain 'response'")
                print("  POST /api/chat         FAIL (no response key)")
        except json.JSONDecodeError:
            errors.append("POST /api/chat: invalid JSON")
            print("  POST /api/chat         FAIL (invalid JSON)")
    elif code == 503:
        print("  POST /api/chat         OK (503 - no API keys; add .env to get 200)")
    else:
        errors.append("POST /api/chat: expected 200 or 503, got %s" % code)
        print("  POST /api/chat         FAIL (HTTP %s)" % code)

    # GET /api/chat.html and /api/health.html
    code, body = req("/api/chat.html")
    if check("GET /api/chat.html", code, 200, "Chat", body):
        print("  GET /api/chat.html     OK (200)")
    else:
        print("  GET /api/chat.html     FAIL")

    code, body = req("/api/health.html")
    if check("GET /api/health.html", code, 200, "health", body):
        print("  GET /api/health.html   OK (200)")
    else:
        print("  GET /api/health.html   FAIL")

    print()
    if errors:
        # If health returned 404, we're likely hitting a static server, not Flask
        if "GET /api/health: expected HTTP 200, got 404" in errors or (errors and "405" in str(errors)):
            print("Tip: Make sure the Flask server is running (not Live Server):")
            print("     python3 server.py")
            print("     Then run this script again.\n")
        print("Errors:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("All API checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
