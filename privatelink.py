#!/usr/bin/env python
# -- coding: utf-8 --

"""
File:           privatelink.py
Author:         Adeel Ahmad
Description:    AWS Lambda function to create PrivateLink.
"""

from cfnresponse import send, SUCCESS, FAILED
import boto3

EC2 = boto3.client('ec2')

def lambder_handler(event, context):
    """
    Handler to build Private-Link
    """
    response = {}

    # There is nothing to do for a delete request
    if event['RequestType'] == 'Delete':
        send(event, context, SUCCESS)
        return

    try:
        privatelink = EC2.create_vpc_endpoint(
            DryRun=event['ResourceProperties']['DryRun'],
            VpcEndpointType=event['ResourceProperties']['VpcEndpointType'],
            VpcId=event['ResourceProperties']['VpcId'],
            ServiceName=event['ResourceProperties']['ServiceName'],
            PolicyDocument=event['ResourceProperties']['PolicyDocument'],
            SubnetIds=event['ResourceProperties']['SubnetIds'],
        )
        response['Data'] = privatelink
        response['Reason'] = 'The PrivateLink was successfully created'

    except Exception:
        response['Status'] = 'FAILED'
        response['Reason'] = 'PrivateLink creation Failed - See \
                CloudWatch logs for the Lamba function backing the custom resource for details'
        send(event, context, FAILED, response['Reason'])

    else:
        send(event, context, SUCCESS, response)
