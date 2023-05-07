#########
# BUILD #
#########
develop:  ## install dependencies and build library
	python -m pip install -e .[develop]
	jupyter nbextension install --py --symlink --overwrite --sys-prefix isedit
	jupyter nbextension enable --py --sys-prefix isedit
	jupyter labextension develop --overwrite isedit

test-develop:
	sudo apt install portaudio19-dev python3-pyaudio
	sudo apt install -y lilypond

build:  ## build the python library
	python setup.py build build_ext --inplace

install:  ## install library
	python -m pip install .

#########
# LINTS #
#########
lint:  ## run static analysis with flake8
	python -m black --check isedit --exclude .ipynb_checkpoints setup.py
	python -m flake8 --exclude .ipynb_checkpoints setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black isedit/ setup.py

# alias
fix: format

check:  ## check assets for packaging
	check-manifest -v

# Alias
checks: check

annotate:  ## run type checking
	python -m mypy ./isedit

#########
# TESTS #
#########
test: ## clean and run unit tests
	python -m pytest -v isedit/tests

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v isedit/tests --cov=isedit --cov-branch --cov-fail-under=75 --cov-report term-missing

# Alias
tests: test



###########
# VERSION #
###########
show-version:
	bump2version --dry-run --allow-dirty setup.py --list | grep current | awk -F= '{print $2}'

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

########
# DIST #
########
dist-build:  # Build python dist
	python setup.py sdist bdist_wheel

dist-check:
	python -m twine check dist/*

dist: clean build dist-build dist-check  ## Build dists

publish:  # Upload python assets
	echo "would usually run python -m twine upload dist/* --skip-existing"


#########
# CLEAN #
#########
deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info .pytest_cache

############################################################################################

TMPREPO=/tmp/docs/bt



docs: 
	$(MAKE) -C docs/ clean
	$(MAKE) -C docs/ html

pages: 
	rm -rf $(TMPREPO)
	git clone -b gh-pages git@github.com:sadigulcelik/isedit.git $(TMPREPO)
	rm -rf $(TMPREPO)/*
	cp -r docs/_build/html/* $(TMPREPO)
	cd $(TMPREPO);\
	git add -A ;\
	git commit -a -m 'auto-updating docs' ;\
	git push
