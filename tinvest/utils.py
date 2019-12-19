def set_default_headers(data, token):
    headers = data.get("headers", {})
    headers.setdefault("accept", "application/json")
    headers.setdefault("Authorization", f"Bearer {token}")
    data["headers"] = headers
