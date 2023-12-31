LICENSE=LICENSE
LICENSE_HEADER?=LICENSE_HEADER
VENV=.venv
$(VENV):
	$(MAKE) install

.PHONY: clean
clean:
	rm -rf .venv

.PHONY: deps-show
deps-show:
	poetry show

.PHONY: deps-show
deps-show-outdated:
	poetry show --outdated

.PHONY: deps-update
deps-update:
	poetry update


.PHONY: install
install: poetry-ensure-installed
	poetry config --local virtualenvs.in-project true
	poetry env use python3.11
	poetry install

.PHONY: format
format: $(VENV)
	poetry run black .

LICENSE:
	@echo "you must have a LICENSE file" 1>&2
	exit 1

LICENSE_HEADER:
	@echo "you must have a LICENSE_HEADER file" 1>&2
	exit 1

.PHONY: license
license: LICENSE LICENSE_HEADER $(VENV)
	poetry run python -m licenseheaders -t ${LICENSE_HEADER} -d serverless/src $(args)
	poetry run python -m licenseheaders -t ${LICENSE_HEADER} -d serverless/test $(args)
	poetry run python -m licenseheaders -t ${LICENSE_HEADER} -d cicd $(args)
	poetry run python -m licenseheaders -t ${LICENSE_HEADER} -d tools $(args)
	poetry run python -m licenseheaders -t ${LICENSE_HEADER} -d word2vec $(args)

.PHONY: build-requirements
build-requirements:
	poetry export --without-hashes --only=main --output=./serverless/requirements.txt
	poetry export --without-hashes --only=main,ai --output=./serverless/requirements-ai.txt

.PHONY: poetry-ensure-installed
poetry-ensure-installed:
	sh ./tools/poetry_ensure_installed.sh

.PHONY: test
test:
	cd serverless && $(MAKE) test

.PHONY: test-not-slow
test-not-slow:
	cd serverless && $(MAKE) test-not-slow

.PHONY: test-all
test-all:
	cd serverless && $(MAKE) test-all

.PHONY: test-all-not-slow
test-all-not-slow:
	cd serverless && $(MAKE) test-all-not-slow

.PHONY: test-format
test-format: $(VENV)
	poetry run black --check .

.PHONY: test-lint
test-lint: $(VENV)
	poetry run flake8 .

.PHONY: test-license
test-license: LICENSE LICENSE_HEADER
	args="--check" $(MAKE) license

.PHONY: test-types
test-types: $(VENV)
	poetry run mypy serverless --exclude fixtures
