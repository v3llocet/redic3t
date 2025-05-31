from __future__ import annotations
import re
from urllib.parse import unquote

class URLAnalyzer:
    def __init__(self, param_patterns, endpoint_patterns, subdomain_patterns):
        self.param_rx = [p if isinstance(p, re.Pattern) else re.compile(p, re.IGNORECASE) for p in param_patterns]
        self.ep_rx    = [p if isinstance(p, re.Pattern) else re.compile(p, re.IGNORECASE) for p in endpoint_patterns]
        self.subd_rx  = [p if isinstance(p, re.Pattern) else re.compile(p, re.IGNORECASE) for p in subdomain_patterns]

    @staticmethod
    def _any(rx_list, text) -> bool:
        return any(rx.search(text) for rx in rx_list)

    def urls(self, url_list: list[str]) -> list[str]:
        return [u for u in url_list if self._any(self.param_rx + self.ep_rx, unquote(u))]

    def parameters(self, param_dict: dict[str, set[str]]):
        hits = []
        for k, vals in param_dict.items():
            for v in vals:
                full = f"{k}={v}"
                if self._any(self.param_rx, full) or self._any(self.param_rx, v):
                    hits.append({"param": k, "value": v})
        return hits

    def endpoints(self, ep_set: set[str]) -> list[str]:
        return [ep for ep in ep_set if self._any(self.ep_rx, ep)]

    def subdomains(self, sd_set: set[str]) -> list[str]:
        return [sd for sd in sd_set if self._any(self.subd_rx, sd)]

    def analyse_all(self, urls, params, endpoints, subdomains):
        return {
            "url_matches":       self.urls(urls),
            "parameter_matches": self.parameters(params),
            "endpoint_matches":  self.endpoints(endpoints),
            "subdomain_matches": self.subdomains(subdomains),
        }
