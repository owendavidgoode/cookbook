PYTHON ?= python3

.PHONY: setup lint test calendar bot book

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

lint:
	$(PYTHON) -m ruff check src tests

test:
	$(PYTHON) -m pytest

calendar:
	$(PYTHON) -m cookbook.cli calendar-validate

bot:
	$(PYTHON) -m cookbook.cli bot-validate

book:
	@echo "Book prep placeholder; hook up chapter dataset generation here."
