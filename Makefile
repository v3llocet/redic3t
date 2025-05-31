.PHONY: install run test 

install:
\tpython -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .

run:
\t. .venv/bin/activate && redic3t $(ARGS)

test:
\t. .venv/bin/activate && pip install pytest && pytest -q
