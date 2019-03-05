import json
import os
import boto3
from fpdf import FPDF

bucketNameParamName = "bucketName"
tmpPathParamName = "tmpPath"
bucketName = os.getenv(bucketNameParamName)
s3 = boto3.client('s3')

def resizePDF(event, context):
    
    prefix = event['queryStringParameters']['prefix']
    compression = event['queryStringParameters']['compression']
    tmpPath = os.getenv(tmpPathParamName)
    print("prefix: " + prefix)
    print("compression: " + compression)
    print("bucketName: " + bucketName)
    
    # Download files
    s3Ressource = boto3.resource('s3')
    bucket = s3Ressource.Bucket(bucketName)
    pdf = FPDF()
    pdf.compress = False
    extensionsAllowed = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG']
    for object in bucket.objects.filter(Prefix=prefix):
        print(object)
        if (object.size > 0):
            path, filename = os.path.split(object.key)
            filenameshort, extension = os.path.splitext(filename)
            if (extension in extensionsAllowed):
                print("path: " + path)
                print("filename: " + filename)
                dest = tmpPath + filename
                print("dest: " + dest)
                bucket.download_file(object.key, dest)
            
                pdf.add_page()
                pdf.image(dest,0,0,210,297)
    
    doc = tmpPath + prefix + ".pdf"
    pdf.output(doc, "F")
    
    destKey = prefix + "/document.pdf"
    bucket.upload_file(doc, destKey)
    
    signedUrlDownload = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucketName,
            'Key': destKey
        },
        ExpiresIn=3600
    )
    
    response = {
        "statusCode": 200,
        "body": {"signedUrlDownload": signedUrlDownload}
    }

    return response
