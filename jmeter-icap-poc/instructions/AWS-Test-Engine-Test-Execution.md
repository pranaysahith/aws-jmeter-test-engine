# AWS Test Engine Test Execution

## AWS Portal

1. Log into the GlasswallAWSCloudSDK-Perf AWS Accout
2. Ensure you are on the eu-west-1 (Ireland) region

### Starting and accessing the Test Engine Dashboard

1. Navigate to the EC2 service then to instances
2. Select the instance AWS-TestEngine-Dashboard
3. Click Actions
4. Select Instance State
5. Click Start Instance
6. After a short wait a public IP Address should appear on the row of that instance Copy this to your clipboard
7. In your browser go to {IP_ADDRESS}:3000, you will land on a grafana login page (NB you must be connected to VPN)
8. Enter the login details
9. Select Dashboards from the left hand menu, then click manage
10. Click on the ICAP Live Performance Dashboard

### Launch Load Generators

If you don't have the aws-jmeter-test-engine-v1 repo from git hub you will need to clone it
``` git clone https://github.com/k8-proxy/aws-jmeter-test-engine-v1.git ```

1. Navigate to the CloudFormation Service
2. Click Create Stack
3. Select 'With New Resources (Standard)'
4. Select Upload a Template File
5. Click Choose File
6. Navigate to ..\aws-jmeter-test-engine-v1\jmeter-icap-poc\cloudformation
7. Select GenerateLoadGenerators.json
8. Click Next
9. Enter a name for the stack (suggested name is AWS-TestEngine-LGs)
10. Click Next
11. Click Next
12. Click Create Stack

You will now be able to go to EC2 Instances, and see the load generators start to spin up.
You will soon start to see data appear on the Grafana Dashboard.

## AWS CLI

1. Go to AWS SSO list https://glasswallsolutions.awsapps.com/start#/
2. Expand GlasswallAWSCloudSDK-Perf AWS Accout
3. Click Command Line or Programatic Access
4. Follow the instructions there to get the access credentials

NB I suggest updating the credentials file located at C:\Users\{username}\.aws in windows or ~/.aws in linux

NB These values update periodically, get the updated values from the AWS SSO list.

### Starting and accessing the Test Engine Dashboard

1. Once you have your credentials set up you can view the state of the dashboard machine with this command
	``` aws ec2 describe-instances --filters "Name=tag:Name,Values=AWS-TestEngine-Dashboard" ```
2. If the instance is showing "State": { "Code": 80, "Name": "stopped" } then you will need to start the instance
3. Take note of the instance Id
4. Run this command to start the instance
	``` aws ec2 start-instances --instance-ids {InstanceId} ```
5. Repeat the command from step 1 to check the updated status
6. Take note of the public IP Address
7. In your browser go to {IP_ADDRESS}:3000, you will land on a grafana login page (NB you must be connected to VPN)
8. Enter the login details
9. Select Dashboards from the left hand menu, then click manage
10. Click on the ICAP Live Performance Dashboard

### Launch Load Generators

1. In your terminal window navigate to ..\aws-jmeter-test-engine-v1\jmeter-icap-poc\cloudformation
2. Run the following command
	``` aws cloudformation create-stack --stack-name AWS-TestEngine-LGs --template-body file://GenerateLoadGenerators.json ```
3. You can view the status of the stack with the following command
	``` aws cloudformation describe-stacks --stack-name AWS-TestEngine-LGs ```
4. You can view the state of started instances by running the following command
	``` aws ec2 describe-instances --filters "Name=tag:Name,Values=LoadTest-1" ```

## Checking values in the Cloudformation Script

It's worth checking a few things in the cloudformation script.

There are some existing resources that the script uses to generate the required instances

ami - ami-07abb328b16a8237a

sg - sg-0c82ddcb24373c694

vpc - vpc-02db6ac5915e8de9b

sn - subnet-02e0fb935c900d08e

key name - AWS-TestEngine-Key

You can check the id values in the script against those shown above.
If you find any discrepancy you can always check the correct values in the portal by looking up the resource.

AMI, Security Group, and Key Pair Name can all be found under the EC2 Service.
VPC and Subnet can be found under the VPC Service.

All resources intended to be used in this script reference AWS-TestEngine in their name.

## Related Resources

### S3 Usage

The S3 Service provides two uses to the test engine.

The S3 bucket used by the test engine is aws-testengine-s3

#### Test Script Storage

The following files are pulled from S3 by the EC2 machines. Any changes to these files will need to be updated in the S3 bucket for a successful test run

- ICAP-POC_s3.jmx
  - S3 Location: s3://aws-testengine-s3/script/ICAP-POC_s3.jmx
  - Purpose: jmx script containing the test to run

- files.txt
  - S3 Location: s3://aws-testengine-s3/script/files.txt
  - Purpose: Conatains a list of files from the test data input folder so the test knows which files to access

- Jmeter Jar files
  - S3 Location: s3://aws-testengine-s3/script/lib/
  - Purpose: Folder which contains the jar files for jmeter plugins used by the jmx script

#### Test Data Storage

This S3 bucket also conatins two locations for Test Data

- s3://aws-testengine-s3/in/
  - This location contains unprocessed files that the jmx script will send to the ICAP Server to be processed

- s3://aws-testengine-s3/out/
  - This location contains processed files that the jmx script has uploaded after the ICAP Server server has processed them
