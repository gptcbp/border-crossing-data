#!/usr/bin/env python3

import csv
import io
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


API_URL = "https://bwt.cbp.gov/api/bwtpublicmod"

RAW_DIR = Path("data/raw/cbp")
RAW_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc)
stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")

json_path = RAW_DIR / f"cbp_{stamp}.json"


def download(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "border-crossing-data/1.0"
        },
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main():
    print(f"Downloading CBP data from {API_URL}")

    raw = download(API_URL)

    # Preserve the exact response received from CBP.
    raw_path = RAW_DIR / f"cbp_{stamp}.raw"
    raw_path.write_bytes(raw)

    print(f"Saved raw response: {raw_path}")

    # Try JSON first.
    try:
        data = json.loads(raw.decode("utf-8-sig"))

        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Saved JSON: {json_path}")
        print("CBP response successfully parsed as JSON.")
        return

    except Exception as exc:
        print(f"JSON parsing failed: {exc}")

    # If CBP changes the format, keep the raw data rather than
    # destroying or replacing it.
    print("Raw CBP response preserved for later parser updates.")


if __name__ == "__main__":
    main()
