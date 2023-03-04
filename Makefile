#########
# LINTS #
#########
lint:  ## run static analysis with flake8
	python -m black --check src setup.py
	python -m flake8 src setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black src/ setup.py

# alias
fix: format

check:  ## check assets for packaging
	check-manifest -v

# Alias
checks: check

annotate:  ## run type checking
	python -m mypy ./src

#########
# TESTS #
#########
test: ## clean and run unit tests
	python -m pytest -v src/tests

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v src/tests --cov=src --cov-branch --cov-fail-under=75 --cov-report term-missing

# Alias
tests: test
