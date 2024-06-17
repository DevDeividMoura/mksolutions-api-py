import httpx

DEFAULT_TIMEOUT = httpx.Timeout(timeout=600.0, connect=5.0)
