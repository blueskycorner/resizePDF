import json
import os
import boto3
from fpdf import FPDF
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from botocore.exceptions import ClientError

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
    
def sendEmail(emailFrom, emailTo, downloadUrl):
   print("address: " + emailTo)
   print("downloadUrl: " + downloadUrl)
   
   SENDER = emailFrom
   RECIPIENT = emailTo
   
   # The subject line for the email.
   SUBJECT = "Your PDF file is ready !"
   
   # The email body for recipients with non-HTML email clients.
   BODY_TEXT = "Hi,\n\nHere is a link to download your file:\n" + downloadUrl + "\n\nHave a nice day."
   
   # The HTML body of the email.
   BODY_HTML = """\
   <html>
   <head></head>
   <body>
   Hi,<br><br>
   Here is a link to download your document: <a href="
   """
   
   BODY_HTML += downloadUrl
   
   BODY_HTML += """\
   ">Click here</a>
   <br><br>
   Have a nice day.<br>
   </body>
   </html>
   """
   
   # The character encoding for the email.
   CHARSET = "utf-8"
   
   # Create a new SES resource and specify a region.
   client = boto3.client('ses')
   
   # Create a multipart/mixed parent container.
   msg = MIMEMultipart('mixed')
   # Add subject, from and to lines.
   msg['Subject'] = SUBJECT 
   msg['From'] = SENDER 
   msg['To'] = RECIPIENT
   
   # Create a multipart/alternative child container.
   msg_body = MIMEMultipart('alternative')
   
   # Encode the text and HTML content and set the character encoding. This step is
   # necessary if you're sending a message with characters outside the ASCII range.
   textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
   htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET) 
   
   # Add the text and HTML parts to the child container.
   msg_body.attach(textpart)
   msg_body.attach(htmlpart)
   
   # Attach the multipart/alternative child container to the multipart/mixed
   # parent container.
   msg.attach(msg_body)
   
   #print(msg)
   try:
      #Provide the contents of the email.
      response = client.send_raw_email(
          Source=SENDER,
          Destinations=[
              RECIPIENT
          ],
          RawMessage={
              'Data':msg.as_string(),
          }
          # ConfigurationSetName=CONFIGURATION_SET
      )
   # Display an error if something goes wrong.	
   except ClientError as e:
      print(e.response['Error']['Message'])
   else:
      print("Email sent! Message ID:")
      print(response['MessageId'])

def resizePDF(event, context):
    
    response = None
    try:
        emailAddress = event['queryStringParameters']['emailAddress']
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
        
        # Send the email
        sendEmail(emailAddress, emailAddress, signedUrlDownload)
        
        response = {
            "statusCode": 200
        }
    except Exception as e:
        response = {
        "statusCode": 500,
        "body": {"error": str(e)}
        }

    return response
