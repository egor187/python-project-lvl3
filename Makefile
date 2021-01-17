install:
	poetry install

check:
	poetry check

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=page_loader/tests -vv --cov-report xml

#.PHONY: install test lint check build
