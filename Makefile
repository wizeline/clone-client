lint:
	@pip install black isort flake8
	@echo "\n--->Sorting imports"
	@isort .
	@echo "\n----->Formating code"
	@black .
	@echo "\n------>Linting code"
	@flake8 .

test:
	@pip3 install coverage pytest
	@coverage run -m pytest
	@coverage report
.PHONY: test 