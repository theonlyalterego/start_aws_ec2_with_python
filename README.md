# Start AWS ES2 Instance with Python Script
This is a simple script to start an EC2 instance in AWS by name.

# How to use

## setup aws credentials

configure your `~/.aws/config` and `~/.aws/credentials` correctly this uses the default aws creds.

## install python3 script requirements

install requirements:
```
 boto3
 argparse
```
## run the script


`python3 start.py --name <name of ec2 instance>`

