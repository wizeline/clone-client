# clone-template-lambdas-python

> **Warning**
>
> This is a template, before you start coding make sure to rename the following files with you project name
>
> 1. The Sonar Project name in ```sonar-project.properties```
> 1. The project references in ```template.yaml```
> 1. The Github actions names in ```.github/workflows```

This project contains the source of a tool for the ClonAI main project

```bash
.
├── Makefile                    <-- Make to automate build
├── README.md                   <-- This instructions file
├── lambdas                     <-- Lambda definition directory
│   └── default                 <-- Default lambda directory
│      └── app.py               <-- Lambda function code
├── shared_layer                <-- Lambda layer directory
│   └── python                  <-- Content of the layer
├── test                        <-- Tests directory
└── template.yaml               <-- SAM-CLI template definition
```

## Requirements

* AWS CLI already configured with Administrator permission
* [Docker installed](https://www.docker.com/community-edition)
* [Python](https://www.python.org/)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Setup process

### Set Environments

Make a copy of the envs file and replace the content with your access tokens

```bash
cp .env.copy .env
```

|Parameter|Description|
| - | - |
|STAGE|Stage identifier|

### Installing dependencies & building the target

In this example we use the built-in `sam build` to automatically download all the dependencies and package our build target.
Read more about [SAM Build here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html)

The `sam build` command is wrapped inside of the `Makefile`. To execute this simply run

```shell
make build
```

## Packaging and deployment

To deploy the application, run the following in your shell:

```bash
make deploy STAGE=stage PROJECT_NAME=project_name
```

### Parameters

|Parameter|Description|Default Value|Example
| :-|:-:| :- | :- |
|stage|Stage name to be used on the deploy process|dev|["dev", "prod"]
|project_name|Prefix to be used in the aws cloud formation stack name|clone-template-lambdas|any|
