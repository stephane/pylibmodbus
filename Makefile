.ONESHELL:
.PHONY: install
install:
	pip install .

.ONESHELL:
.PHONY: build
build: install
	python -m pip install --upgrade build twine
	python -m build

.ONESHELL:
.PHONY: publish
publish: build
	python -m twine upload dist/*
