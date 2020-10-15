#!/usr/bin/env python
# coding: utf-8

import boto3
from math import ceil
import argparse
from datetime import datetime


def main():

    # Load configuration
    try:
        with open("config.env") as f:
            config = f.readlines()
        configuration = dict(c.strip().split("=") for c in config)
    except Exception as e:
        print("Please create config.env file similar to config.env.sample")
        print(str(e))
        raise

    # Authenticate to aws
    profile = configuration.get("aws_profile_name")
    session = boto3.session.Session(profile_name=profile)
    client = session.client('cloudformation')

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
    if total_users <= users_per_instance:
        instances_required = 1
    else:
        i = 0
        while i < 5:
            if total_users % users_per_instance == 0:
                instances_required = int(total_users/users_per_instance)
                break
            else:
                if total_users % instances_required == 0:
                    users_per_instance = int(total_users / instances_required)
                else:
                    instances_required += 1
            i += 1

        if instances_required * users_per_instance != total_users:
            print("Please provide total_users in multiples of users_per_instance.")
            exit(0)

    # write the number of instances required to a file in s3 bucket
    s3_client = session.client('s3', region_name="us-west-2")
    bucket = configuration.get("bucket")
    file_name = configuration.get("file_name")
    s3_client.put_object(Bucket=bucket,
                        Body=str(instances_required),
                        Key=file_name)

    # Load cloudformation template
    with open("GenerateLoadGenerators.json", "r") as f:
        asg_template_body = f.read()


    # create ASG with instances to run jmeter tests
    now = datetime.now()
    date_suffix = now.strftime("%Y-%m-%d-%H-%M")
    stack_name = 'aws-jmeter-test-engine-' + date_suffix
    asg_name = "LoadTest-" + date_suffix
    print("Deploying %s instances in the ASG by creating %s cloudformation stack"% (instances_required, stack_name))
    
    client.create_stack(
        StackName=stack_name,
        TemplateBody=asg_template_body,
        Parameters=[
            {
                "ParameterKey": "MinInstances",
                "ParameterValue": str(instances_required)
            },
            {
                "ParameterKey": "MaxInstances",
                "ParameterValue": str(instances_required)
            },
            {
                "ParameterKey": "AsgName",
                "ParameterValue": asg_name
            }
        ]
    )

if __name__ == "__main__":
    main()
