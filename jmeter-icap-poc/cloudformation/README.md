## Create CloudFormation stack to deploy AutoScalingGroup

1. Install python.

2. Install boto3 python package by running below command:

```
pip3 install boto3
```

3. Set the AWS profile to be uesd for authentication.

```
export AWS_DEFAULT_PROFILE=your_profile
```

4. Run below command to get help on the script

```
python3 create_stack.py -h
```

Pass `total_users` and `users_per_instance` as input parameters to the script.

`total_users` is the total number of users for the test. Default value of this parameter is 4000

`users_per_instance` is the number of users per ec2 instance. Default value of this parameter is 4000

Create the stack by running below command:

```
python3 create_stack.py --total_users 4000 --users_per_instance 4000
```

5. Once the tests are completed, delete the stack from AWS console and create stack again when required.

