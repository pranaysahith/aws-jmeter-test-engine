## Create CloudFormation stack to deploy AutoScalingGroup

1. Install python.

2. Install boto3 python package by running below command:

```
pip3 install boto3
```

3. Set AWS authentication.

Get the AWS access key credentails and update in ~/.aws/credentials file for a particular profile. Below is an example of how it should look.

```
[glasswall]
aws_access_key_id = <required value>
aws_secret_access_key = <required value>
aws_session_token = <optional value>
```

Update the ~/.aws/config with the same profile by setting the region you want to use. Below is an example

```
[profile glasswall]
region = eu-west-2
```

4. Run below command to get help on the script

```
python3 create_stack.py -h
```

Pass `total_users` and `users_per_instance` as input parameters to the script.

`total_users` is the total number of users for the test. Default value of this parameter is 4000

`users_per_instance` is the number of users per ec2 instance. Default value of this parameter is 4000

Based on the values passed for total_users and users_per_instance, number of instances required will be calculated. The total users will be equally divided among all the instances.

5. Create config file.

Create config.env file by copying config.env.sample file. Update the file with below details:

- aws_profile_name - The AWS profile created in step 3.
- bucket=gov - Bucket name where a file with number of instances will be created.
- file_name -  File name with number of instances will be created in the s3 bucket.

6. Create the cloudformation stack by running below command:

Linux or Mac:
```bash
export AWS_DEFAULT_PROFILE=your_profile_name
python create_stack.py --total_users 4000 --users_per_instance 4000
```

Windows powershell or command prompt:
```powershell
set AWS_DEFAULT_PROFILE your_profile_name
python create_stack.py --total_users 4000 --users_per_instance 4000
```

7. Once the tests are completed, delete the stack from AWS cloudformation using console and run the script again when required.

