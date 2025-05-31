from __future__ import annotations
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

class URLDataExtractor:
    def __init__(self, urls: list[str]):
        self.urls = urls
        self.query_params = defaultdict(set)
        self.endpoints = set()
        self.subdomains = set()

    def extract_all(self) -> None:
        for url in self.urls:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if hostname:
                self.subdomains.add(hostname)

            path = parsed.path
            if path and path != "/":
                self.endpoints.add(path)

            query = parse_qs(parsed.query)
            for param, values in query.items():
                for value in values:
                    self.query_params[param].add(value)

    def get_subdomains(self) -> set[str]:
        return self.subdomains

    def get_endpoints(self) -> set[str]:
        return self.endpoints

    def get_query_params(self) -> dict[str, set[str]]:
        return dict(self.query_params)
