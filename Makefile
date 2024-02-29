-include .env


PROJECT_NAME=clone-template-lambdas-python
STAGE=dev
FULL_PROJECT_NAME=${PROJECT_NAME}-${STAGE}

.PHONY: build

build:
	@sam build -t template.yaml

deploy: build
	@sam deploy \
		--stack-name ${FULL_PROJECT_NAME} \
		--s3-prefix ${FULL_PROJECT_NAME} \
		--resolve-s3 \
		--parameter-overrides \
			STAGE=${STAGE} \
		--force-upload

delete:
	@sam delete \
		--stack-name ${FULL_PROJECT_NAME}

test:
	@pip3 install coverage pytest
	@coverage run -m pytest
	@coverage report
.PHONY: test 

env:
	@python3 -m venv env
	@pip3 install pipreqs 
	@pipreqs lambdas --force
	@python3 -m pip install -r requirements.txt
.PHONY: env

lint:
	@pip3 install black isort flake8
	@isort lambdas shared_layer
	@black -l 100 lambdas shared_layer
	@flake8 lambdas shared_layer