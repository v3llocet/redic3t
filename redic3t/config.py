from __future__ import annotations
from dataclasses import dataclass
from importlib import resources
import json
import re
from typing import List

@dataclass
class PatternConfig:
    parameter_patterns: List[re.Pattern]
    endpoint_patterns: List[re.Pattern]
    subdomain_patterns: List[re.Pattern]

    @classmethod
    def load_default(cls) -> "PatternConfig":
        with resources.files("redic3t.data").joinpath("regex_patterns.json").open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        def compile_list(items):
            return [p if isinstance(p, re.Pattern) else re.compile(p, re.IGNORECASE) for p in items]
        return cls(
            parameter_patterns = compile_list(data.get("parameter_patterns", [])),
            endpoint_patterns  = compile_list(data.get("endpoint_patterns", [])),
            subdomain_patterns = compile_list(data.get("subdomain_patterns", [])),
        )
