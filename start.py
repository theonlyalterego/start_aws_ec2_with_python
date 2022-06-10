import boto3
import argparse
import time

client = boto3.client("ec2")


def get_state(instance_name):
    """get_state: get the state of the ec2 instance by name."""
    filters = [
        {
            "Name": "tag:Name",
            "Values": [instance_name],
        }
    ]

    response = client.describe_instances(Filters=filters)

    instances = (
        instance
        for reservation in response["Reservations"]
        for instance in reservation["Instances"]
    )

    for instance in instances:
        tags = (tag for tag in instance["Tags"])
        tag_ar = []
        for tag in tags:
            tag_ar.append(tag["Value"])
        tag_str = " ".join(tag_ar)
        id = instance["InstanceId"]
        state = instance["State"]["Name"]

    return id, tag_str, state


def startup(instance_name):
    """startup: start the ec2 instance by name."""

    id, tag_str, state = get_state(instance_name)
    print(tag_str + " : " + id + " : " + state)
    starting_state = state
    if state == "stopping":
        while state != "stopped" or state == starting_state:
            print("waiting 5s to check state...")
            time.sleep(5)
            print(tag_str + " : " + id + " : " + state)
            id, tag_str, state = get_state(instance_name)

    if state != "running":
        starting_state = state
        print("Starting instance...")
        start_response = client.start_instances(
            InstanceIds=[
                id,
            ]
        )
        c_states = (state for state in start_response["StartingInstances"])
        while state != "running" or state == starting_state:
            print("waiting 5s to check state...")
            time.sleep(5)
            print(tag_str + " : " + id + " : " + state)
            id, tag_str, state = get_state(instance_name)

        # print('Starting instance...')
        # start_response = client.start_instances(
        #     InstanceIds=[
        #         id,
        #     ]
        # )
        # c_states = (state
        #               for state in start_response['StartingInstances'])

        for c_state in c_states:
            print("now: " + c_state["CurrentState"]["Name"])
    else:
        print("Already (" + state + ") no action needed.")


parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, required=True)
args = parser.parse_args()
startup(args.name)
