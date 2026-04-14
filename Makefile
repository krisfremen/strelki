.PHONY: auto sync sync38 sync39 sync310 sync311 sync312 sync313 sync314 test lint typecheck lint-docs docs clean clean-docs clean-dist live-docs build-dist install-hooks

auto: sync311

sync38: UV_PYTHON = 3.8
sync39: UV_PYTHON = 3.9
sync310: UV_PYTHON = 3.10
sync311: UV_PYTHON = 3.11
sync312: UV_PYTHON = 3.12
sync313: UV_PYTHON = 3.13
sync314: UV_PYTHON = 3.14

sync sync38 sync39 sync310 sync311 sync312 sync313 sync314:
	uv sync --python $(or $(UV_PYTHON),3.11) --all-extras

install-hooks:
	uv run --extra test pre-commit install

test:
	rm -f .coverage coverage.xml
	uv run --extra test pytest

lint:
	uv run --extra test pre-commit run --all-files --show-diff-on-failure

typecheck:
	uv run --extra test ty check

lint-docs:
	uv run --all-extras doc8 docs/index.rst README.rst --extension .rst --ignore D001
	uv run --all-extras --directory docs make html

clean-docs:
	rm -rf docs/_build

docs:
	uv run --all-extras --directory docs make html

live-docs: clean-docs
	uv run --extra doc sphinx-autobuild docs docs/_build/html

clean: clean-dist
	rm -rf .venv venv .pytest_cache ./**/__pycache__
	rm -f .coverage coverage.xml ./**/*.pyc

clean-dist:
	rm -rf dist build *.egg *.eggs *.egg-info

build-dist: clean-dist
	uv build
