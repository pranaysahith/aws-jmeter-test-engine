# Setup github actions to run jmeter tests on AWS

## Authentication to AWS 

Workflows in Github Actions can authenticate to AWS using AWS credentails.

Github secrets should be used to store the AWS credentails.

The following secrets should be created in github secrets

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

Once the secrets are created, they can be used for authentication in the workflow using `actions/configure-aws-credentials@v1` action.

## Execute tests

Any steps followed by above authentication step will have access to AWS.

As we are using python to deploy the infrastructure to AWS and run the tests, we need to install python using `actions/setup-python@v1` action.

Once python is installed we can run the python script to execute the tests.

## Schedule the workflow

The workflow can be scheduled to run the tests at periodic intervals using a cron.
