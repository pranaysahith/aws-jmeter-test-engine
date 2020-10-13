#!/usr/bin/env python
# coding: utf-8

import boto3
from math import ceil
import argparse


def main():

    client = boto3.client('cloudformation')

    parser = argparse.ArgumentParser(description='Create cloudformation stack to deploy ASG.')
    parser.add_argument('--total_users', '-t',
                        help='total number of users in the test (default: 4000)')

    parser.add_argument('--users_per_instance', '-u',
                        help='number of users per instance (default: 4000)')

    args = parser.parse_args()
    
    if args.total_users:
        total_users = int(args.total_users)
    else:
        total_users = 4000

    if args.users_per_instance:
        users_per_instance = int(args.users_per_instance)
    else:
        users_per_instance = 4000
    
    # calculate number of instances required
    instances_required = ceil(total_users/users_per_instance)

    # Load cloudformation template
    with open("GenerateLoadGenerators.json", "r") as f:
        asg_template_body = f.read()


    # create ASG with instances to run jmeter tests
    print("Deploying %s instances in the ASG"%instances_required)
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
