# redic3t 

Passive reconnaissance using the Wayback Machine.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .

# run 
redic3t example.com

```

## Project layout

- `src/redic3t/` — package code 
- `src/redic3t/data/regex_patterns.json` — bundled regex rules
- `tests/` — pytest tests

## Dev helpers

```bash
make install    
make run ARGS="example.com"
make test
```
