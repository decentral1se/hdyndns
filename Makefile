PIPENV := pipenv run

publish:
	@rm -rf dist
	@$(PIPENV) python setup.py bdist_wheel
	@$(PIPENV) twine upload dist/*
