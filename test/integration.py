import sys
sys.path.append('.')
import os
from buildSignedUrlUpload import buildSignedUrlUpload
import resizePDF
import requests
import uuid

buildSignedUrlUploadPath = '/buildSignedUrlUpload'
resizePDFPath = '/resizePDF'
imagesList = ["test/Data/2016-06_Alex_CP_Bulletin1ertrim-page1.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page2.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page3.jpg"]
compression = '50'
emailAddress = 'benjamin.ehlers@hardis.fr'

def integration(serviceEndpoint):
    try:
        buildSignedUrlUpload_URL = serviceEndpoint + buildSignedUrlUploadPath
        resizePDF_URL = serviceEndpoint + resizePDFPath
        
        id = uuid.uuid4()
        
        for image in imagesList:
            path, filename = os.path.split(image)
            PARAMS = {'prefix':id, 'filename': filename} 
            r = requests.get(url = buildSignedUrlUpload_URL, params = PARAMS) 
      
            # extracting data in json format 
            data = r.json()
            signedUrlUpload = data['signedUrlUpload']
            r = requests.put(signedUrlUpload, data=open(image, 'rb'))
            print("buildSignedUrlUpload_URL: " + str(r.status_code))
        
        PARAMS = {'prefix':id, 'compression': compression, 'emailAddress': emailAddress} 
        r = requests.get(url = resizePDF_URL, params = PARAMS)
        print("resizePDF: " + str(r.status_code))
    except Exception as e:
        print(str(e))
        raise e
   
        
if __name__ == "__main__":
    try:
        serviceEndpoint = sys.argv[1] # 'https://kwkkg3ml2j.execute-api.us-east-1.amazonaws.com/dev'
        integration(serviceEndpoint)
    except Exception as e:
        print(str(e))
        exit(1)