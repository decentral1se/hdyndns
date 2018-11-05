PIPENV := pipenv run

publish:
	@rm -rf dist
	@$(PIPENV) python setup.py sdist
	@$(PIPENV) twine upload dist/*
