#!/usr/bin/env python
# coding: utf-8

import boto3
from math import ceil


def main():

    client = boto3.client('cloudformation')

    # calculate number of instances required
    total_users = 4000
    users_per_instance = 4000
    instances_required = ceil(total_users/users_per_instance)


    # Load cloudformation template
    with open("jmeter-icap-poc/cloudformation/GenerateLoadGenerators.json", "r") as f:
        asg_template_body = f.read()


    # create ASG with instances to run jmeter tests
    client.create_stack(
        StackName='aws-jmeter-test-engine-v1-asg',
        TemplateBody=asg_template_body,
        Parameters=[
            {
                "ParameterKey": "MinInstances",
                "ParameterValue": str(instances_required)
            },
            {
                "ParameterKey": "MaxInstances",
                "ParameterValue": str(instances_required)
            }
        ]
    )

if __name__ == "__main__":
    main()
