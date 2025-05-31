from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import sys

from .wayback import WaybackMachineClient
from .extractor import URLDataExtractor
from .analyzer import URLAnalyzer
from .config import PatternConfig

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="redic3t",
        description="Passive reconnaissance (Wayback archives)",
    )
    p.add_argument("domain", help="Target domain (e.g. example.com)")
    p.add_argument("-o", "--output", type=Path, help="Write results to file (.txt or .json)")
    p.add_argument("-v", "--verbose", action="store_true", help="List every individual match on stdout")
    return p.parse_args()

def _banner(text: str) -> None:
    print(f"\n{'=' * 60}\n{text}\n{'=' * 60}")

def _print_set(label: str, items) -> None:
    print(f"\n[+] {label} ({len(items)})")
    for itm in items:
        print(f"    {itm}")

def main() -> None:
    args = parse_args()

    # load regex patterns from package data
    cfg = PatternConfig.load_default()
    print(f"[i] Loaded regex sets  –  params:{len(cfg.parameter_patterns)}  endpoints:{len(cfg.endpoint_patterns)}  subdomains:{len(cfg.subdomain_patterns)}")

    # fetch archived URLs
    client = WaybackMachineClient(args.domain)
    try:
        urls = client.fetch_archived_urls()
    except Exception as exc:
        sys.exit(f"[!] Wayback fetch failed: {exc}")

    if not urls:
        sys.exit("[!] No archived URLs returned – terminating.")

    print(f"[✔] Retrieved {len(urls)} archived URL(s)")

    # extract artefacts
    extractor = URLDataExtractor(urls)
    extractor.extract_all()
    subdomains = extractor.get_subdomains()
    endpoints  = extractor.get_endpoints()
    params     = extractor.get_query_params()

    analyzer = URLAnalyzer(cfg.parameter_patterns, cfg.endpoint_patterns, cfg.subdomain_patterns)
    results = analyzer.analyse_all(urls, params, endpoints, subdomains)

    # summary
    _banner("Extraction summary")
    _print_set("Sub-domains", subdomains)
    _print_set("Endpoints", endpoints)
    total_param_vals = sum(len(v) for v in params.values())
    print(f"\n[+] Parameters collected: {total_param_vals} values across {len(params)} keys")
    for k, v in {k: sorted(v) for k, v in params.items()}.items():
        print(f"+_+ {k}:")
        for e in v:
            print(f"     {e}")

    _banner("Redirect-pattern matches")
    for key in ("url_matches", "parameter_matches", "endpoint_matches", "subdomain_matches"):
        print(f"    {key.replace('_', ' ').title():20}: {len(results[key])}")
    if args.verbose:
        for key, hits in results.items():
            if hits:
                _print_set(key.replace('_', ' ').title(), hits)

    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            if args.output.suffix.lower() == ".json":
                payload = {
                    "scanned_domain": args.domain,
                    "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                    "extracted": {
                        "subdomains": sorted(subdomains),
                        "endpoints":  sorted(endpoints),
                        "parameters": {k: sorted(v) for k, v in params.items()},
                    },
                    "matches": results,
                }
                args.output.write_text(json.dumps(payload, indent=2))
            else:
                with args.output.open("w", encoding="utf-8") as fh:
                    fh.write(f"# Wayback Redirect Scanner – {args.domain}\n")
                    fh.write(f"# Generated: {datetime.utcnow().isoformat()}Z\n\n")
                    fh.write("## Extraction\n")
                    for title, coll in (("Sub-domains", subdomains), ("Endpoints", endpoints)):
                        fh.write(f"\n### {title} ({len(coll)})\n")
                        for itm in sorted(coll):
                            fh.write(f"- {itm}\n")
                    fh.write("\n### Parameters\n")
                    for p, vals in params.items():
                        for val in vals:
                            fh.write(f"- {p} = {val}\n")
                    fh.write("\n## Matches\n")
                    for cat, hits in results.items():
                        fh.write(f"\n### {cat} ({len(hits)})\n")
                        for h in hits:
                            fh.write(f"- {h}\n")
            print(f"\n[✔] Results saved to {args.output}")
        except Exception as exc:
            print(f"[!] Failed to write results: {exc}")

if __name__ == "__main__":
    main()
