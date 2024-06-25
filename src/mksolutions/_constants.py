import httpx

DEFAULT_TIMEOUT = httpx.Timeout(timeout=600.0, connect=5.0)
RAW_RESPONSE_HEADER = "X-Stainless-Raw-Response"

