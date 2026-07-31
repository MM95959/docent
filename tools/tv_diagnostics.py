#!/usr/bin/env python3

import json
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

DOCENT_URL = "http://localhost:8000"


def get_json(path: str) -> dict:
    url = f"{DOCENT_URL}{path}"

    try:
        with urlopen(url, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{url} returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(
            f"Could not reach Docent at {DOCENT_URL}: {exc.reason}"
        ) from exc


def main() -> int:
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    try:
        info = get_json("/api/info")
        art = get_json("/api/art")
    except RuntimeError as exc:
        print(f"Diagnostic failed: {exc}", file=sys.stderr)
        return 1

    items = art.get("items") or []

    report = {
        "timestamp": timestamp,
        "docent_url": DOCENT_URL,
        "tv_supported": info.get("supported"),
        "tv_ip": info.get("ip"),
        "art_api_version": info.get("api_version"),
        "artmode": info.get("artmode"),
        "current_artwork_id": art.get("current_id"),
        "artwork_count": len(items),
        "art_cache_stale": art.get("stale", False),
    }

    print("Docent TV diagnostic — read only")
    print("--------------------------------")
    print(json.dumps(report, indent=2))
    print()
    print("No TV settings or artwork were changed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
