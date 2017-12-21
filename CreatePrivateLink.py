#!/usr/bin/env python
# -- coding: utf-8 --

"""
File:           CreatePrivateLink.py
Author:         Adeel Ahmad
Github:         https://github.com/adeelahmad84
Description:    AWS Lambda to run aws-cli for PrivateLink
"""

from __future__ import print_function
import boto3
import os
import sys

ec2 = boto3.client('ec2')

def send_response(request, response, status=None, reason=None):
    """ Send our response to the pre-signed URL supplied by CloudFormation
    If no ResponseURL is found in the request, there is no place to send a
    response. This may be the case if the supplied event was for testing.
    """

    if status is not None:
        response['Status'] = status

    if reason is not None:
        response['Reason'] = reason

    if 'ResponseURL' in request and request['ResponseURL']:
        url = urlparse.urlparse(request['ResponseURL'])
        body = json.dumps(response)
        https = httplib.HTTPSConnection(url.hostname)
        https.request('PUT', url.path+'?'+url.query, body)

    return response

def handler(event, context):
    """
    Invoke aws-cli
    """
    response = {
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Status': 'SUCCESS'
            }

    # PhysicalResourceId is meaningless here, but CloudFormation requires it
    if 'PhysicalResourceId' in event:
        response['PhysicalResourceId'] = event['PhysicalResourceId']
    else:
        response['PhysicalResourceId'] = str(uuid.uuid4())

    # There is nothing to do for a delete request
    if event['RequestType'] == 'Delete':
        return send_response(event, response)

    try:
        privatelink = ec2.create_vpc_endpoint(
                DryRun=event['ResourceProperties']['DryRun']
                VpcEndpointType=event['ResourceProperties']['VpcEndpointType']
                VpcId=event['ResourceProperties']['VpcId']
                ServiceName=event['ResourceProperties']['ServiceName']
                PolicyDocument=event['ResourceProperties']['PolicyDocument']
                SubnetIds=event['ResourceProperties']['SubnetIds']
                ClientToken=event['ResourceProperties']['ClientToken']
                PrivateDnsEnabled=event['ResourceProperties']['PrivateDnsEnabled']
                )

        response['Data'] = {
                
                }



