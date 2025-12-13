.PHONY: help install test test-update clean update-deps upgrade-deps

help:
	@echo "Available targets:"
	@echo "  install        - Install dependencies from requirements.txt"
	@echo "  test           - Run all tests"
	@echo "  test-update    - Run tests and update snapshots"
	@echo "  update-deps    - Update requirements.txt with latest versions"
	@echo "  upgrade-deps   - Upgrade all installed packages and update requirements.txt"
	@echo "  clean          - Remove temporary files and caches"

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest tests/ -v

test-update:
	python -m pytest tests/ -v --snapshot-update

update-deps:
	python -m pip install --upgrade pip
	python -m pip install --upgrade -r requirements.txt
	python -m pip freeze > requirements.txt

upgrade-deps:
	python -m pip install --upgrade pip
	python -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 python -m pip install --upgrade || true
	python -m pip freeze > requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
