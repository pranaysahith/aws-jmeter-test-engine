#!/usr/bin/env python
# coding: utf-8

import boto3
from math import ceil
import argparse
from datetime import datetime
import re
import os


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
    profile = os.getenv("AWS_PROFILE_NAME", configuration.get("aws_profile_name"))
    session = boto3.session.Session(profile_name=profile)
    client = session.client('cloudformation')

    parser = argparse.ArgumentParser(description='Create cloudformation stack to deploy ASG.')
    parser.add_argument('--total_users', '-t', default=4000,
                        help='total number of users in the test (default: 4000)')

    parser.add_argument('--users_per_instance', '-u', default=4000,
                        help='number of users per instance (default: 4000)')

    parser.add_argument('--ramp_up', '-r', default=300,
                        help='ramp up time (default: 300)')

    parser.add_argument('--duration', '-d', default=900,
                        help='duration of test (default: 900)')

    parser.add_argument('--endpoint_url', '-e', default="gw-icap01.westeurope.azurecontainer.io",
                        help='ICAP server endpoint URL (default: gw-icap01.westeurope.azurecontainer.io)')

    args = parser.parse_args()
    
    total_users = int(args.total_users)
    users_per_instance = int(args.users_per_instance)
    ramp_up = args.ramp_up
    duration = args.duration
    endpoint_url = args.endpoint_url
    
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

    # write the script to s3 bucket after updating the parameters
    with open("script.sh") as f:
        script_data = f.read()
    
    script_data = re.sub("-Jp_vuserCount=[0-9]*", "-Jp_vuserCount=" + str(users_per_instance), script_data)
    script_data = re.sub("-Jp_rampup=[0-9]*", "-Jp_rampup=" + str(ramp_up), script_data)
    script_data = re.sub("-Jp_duration=[0-9]*", "-Jp_duration=" + str(duration), script_data)
    script_data = re.sub("-Jp_url=[a-zA-Z0-9\-\.]*", "-Jp_url=" + str(endpoint_url), script_data)

    s3_client = session.client('s3')
    bucket = os.getenv("BUCKET", configuration.get("bucket"))
    file_name = os.getenv("FILE_NAME", configuration.get("file_name"))
    s3_client.put_object(Bucket=bucket,
                        Body=script_data,
                        Key=file_name)

    # Load cloudformation template
    with open("GenerateLoadGenerators.json", "r") as f:
        asg_template_body = f.read()


    # create ASG with instances to run jmeter tests
    now = datetime.now()
    date_suffix = now.strftime("%Y-%m-%d-%H-%M")
    stack_name = 'aws-jmeter-test-engine-' + date_suffix
    asg_name = "LoadTest-" + date_suffix

    # Determine the size of ec2 instance
    if 0 < users_per_instance < 1000:
        instance_type = "m4.large"
    elif 1000 <= users_per_instance < 2500:
        instance_type = "m4.xlarge"
    elif 2500 <= users_per_instance <= 4000:
        instance_type = "m4.2xlarge"
    else:
        instance_type = "m4.2xlarge"

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
            },
            {
                "ParameterKey": "InstanceType",
                "ParameterValue": instance_type
            }
        ]
    )

if __name__ == "__main__":
    main()
