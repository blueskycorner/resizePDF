import json
import os
import boto3

bucketNameParamName = "bucketName"
tmpPathParamName = "tmpPath"
bucketName = os.getenv(bucketNameParamName)
s3 = boto3.client('s3')

def buildSignedUrlUpload(event, context):
    try:
        print(event)
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
    
        responseBody = {"signedUrlUpload": signedUrlUpload}
        response = {
            "statusCode": 200,
            "body": json.dumps(responseBody),
            "headers": {"Access-Control-Allow-Origin": "*"},
            "isBase64Encoded": "false"
        }
    except Exception as e:
        responseBody = {"error": str(e)}
        response = {
            "statusCode": 500,
            "body": json.dumps(responseBody)
        }
    

    return response