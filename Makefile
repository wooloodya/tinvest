
.PHONY: init test lint pretty precommit_install bump_major bump_minor bump_patch

BIN = .venv/bin/

CODE = tinvest

init:
	python3 -m venv .venv
	poetry install

test:
	$(BIN)pytest --verbosity=2 --showlocals --strict --log-level=DEBUG --cov=$(CODE) $(args)

lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(CODE) tests
	$(BIN)pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(BIN)black --skip-string-normalization --line-length=88 --check $(CODE) tests
	$(BIN)pytest --dead-fixtures --dup-fixtures
	$(BIN)mypy $(CODE) tests

pretty:
	$(BIN)isort --apply --recursive $(CODE) tests
	$(BIN)black --skip-string-normalization --line-length=88 $(CODE) tests
	$(BIN)unify --in-place --recursive $(CODE) tests

precommit_install:
	echo '#!/bin/sh\nmake lint test\n' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

bump_major:
	$(BIN)bumpversion major

bump_minor:
	$(BIN)bumpversion minor

bump_patch:
	$(BIN)bumpversion patch