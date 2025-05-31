from __future__ import annotations
import requests
import json

class WaybackMachineClient:
    def __init__(self, domain: str):
        self.domain = domain
        self.headers = {"User-Agent": "Mozilla/5.0 (redic3t)"}
        self.url = (
            f"https://web.archive.org/cdx/search?url={domain}%2F&matchType=prefix"
            "&collapse=urlkey&output=json"
            "&fl=original&filter=!statuscode:[45]..&limit=100000"
        )

    def fetch_archived_urls(self) -> list[str]:
        resp = requests.get(self.url, headers=self.headers, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Wayback fetch failed: {resp.status_code}")
        data = json.loads(resp.text)
        return [row[0] for row in data[1:]]
