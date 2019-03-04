import json
import os
import boto3
import requests

bucketNameParamName = "bucketName"
bucketName = os.getenv(bucketNameParamName)
s3 = boto3.client('s3')

def buildSignedUrlUpload(event, context):
    signedUrlUpload = ""
    prefix = event['queryStringParameters']['prefix']
    filename = event['queryStringParameters']['filename']
    print("prefix: " + prefix)
    print("filename: " + filename)
    print("bucketName: " + bucketName)
    
    signedUrlUpload = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucketName,
            'Key': prefix + '/' + filename
        },
        ExpiresIn=3600
    )
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event['queryStringParameters']
    }

    response = {
        "statusCode": 200,
        "body": {"signedUrlUpload": signedUrlUpload}
    }

    return response
