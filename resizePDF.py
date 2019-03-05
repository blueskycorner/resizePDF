import json
import os
import boto3
from fpdf import FPDF

bucketNameParamName = "bucketName"
tmpPathParamName = "tmpPath"
bucketName = os.getenv(bucketNameParamName)
s3 = boto3.client('s3')

def buildPDF(filename, imagesList):
    try:
        pdf = FPDF()
        pdf.compress = False
        print("Nb images to add: " + str(len(imagesList)))
        for image in imagesList:
            pdf.add_page()
            pdf.image(image,0,0,210,297)
            
        pdf.output(filename)
    except Exception as e:
        print(e)
        raise e
    

def resizePDF(event, context):
    
    response = None
    try:
        prefix = event['queryStringParameters']['prefix']
        compression = event['queryStringParameters']['compression']
        tmpPath = os.getenv(tmpPathParamName)
        print("prefix: " + prefix)
        print("compression: " + compression)
        print("bucketName: " + bucketName)
        
        # Download files and build 
        s3Ressource = boto3.resource('s3')
        bucket = s3Ressource.Bucket(bucketName)
        extensionsAllowed = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
        
        imagesList = []
        for object in bucket.objects.filter(Prefix=prefix):
            print(object)
            if (object.size > 0):
                path, filename = os.path.split(object.key)
                filenameshort, extension = os.path.splitext(filename)
                print("path: " + path)
                print("filename: " + filename)
                print("filenameshort: " + filenameshort)
                print("extension: " + extension)
                if (extension in extensionsAllowed):
                    print("path: " + path)
                    print("filename: " + filename)
                    dest = tmpPath + filename
                    print("dest: " + dest)
                    bucket.download_file(object.key, dest)
                
                    imagesList.append(dest)
        
        # Build the PDF
        doc = tmpPath + prefix + ".pdf"
        buildPDF(doc, imagesList)
        
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
    except Exception as e:
        response = {
        "statusCode": 500,
        "body": {"error": str(e)}
        }

    return response
