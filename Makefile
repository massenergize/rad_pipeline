.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

export DOCKER=docker
export PWD=`pwd`

MODE ?= dev
export JUPYTER_HOST_PORT ?= 8888
export JUPYTER_CONTAINER_PORT ?= $(JUPYTER_HOST_PORT)
export PROJECT_NAME=rad_pipeline
export BASE_DOCKERFILE=docker/base/Dockerfile
export DOCKERFILE=docker/$(MODE)/Dockerfile
export BASE_IMAGE_NAME=$(PROJECT_NAME)-image-base
export IMAGE_NAME=$(PROJECT_NAME)-$(MODE)-image
export CONTAINER_NAME=$(PROJECT_NAME)-$(MODE)-container

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

export CURRENT_UID
export CURRENT_GID


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docker ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-data:
	rm data/clean/*.pkl
	rm data/output/*.parquet

lint: ## check style with flake8
	flake8 rad_pipeline tests
	mypy rad_pipeline

test: ## run tests quickly with the default Python
	pytest


test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source rad_pipeline -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/rad_pipeline.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ rad_pipeline
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

init: init-docker sync-from-source ## initialize repository for traning

sync-from-source: ## download data data source to local envrionment
	@echo "Data sync from source not yet implemented..."

init-docker: ## initialize docker image
	$(DOCKER) build -t $(BASE_IMAGE_NAME) -f $(BASE_DOCKERFILE) --build-arg UID=$(shell id -u) .
	$(DOCKER) build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

init-docker-no-cache: ## initialize docker image without cache
	$(DOCKER) build --no-cache -t $(BASE_IMAGE_NAME) -f $(BASE_DOCKERFILE) --build-arg UID=$(shell id -u) .
	$(DOCKER) build --no-cache -t $(IMAGE_NAME) -f $(DOCKERFILE) .

create-container: ## create docker container
	$(DOCKER) run -it -v $(PWD):/app -p $(JUPYTER_HOST_PORT):$(JUPYTER_CONTAINER_PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

clean-container: ## remove Docker container
	-$(DOCKER) rm $(CONTAINER_NAME)

clean-image: ## remove Docker image
	-$(DOCKER) image rm $(IMAGE_NAME)

clean-docker: clean-container clean-image ## remove Docker image and container
