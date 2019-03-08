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
print (sys.path)
def integration(serviceEndpoint):
    buildSignedUrlUpload_URL = serviceEndpoint + buildSignedUrlUploadPath
    resizePDF_URL = serviceEndpoint + resizePDFPath
    
    for image in imagesList:
        id = uuid.uuid4()
        path, filename = os.path.split(image)
        PARAMS = {'prefix':id, 'filename': filename} 
        r = requests.get(url = buildSignedUrlUpload_URL, params = PARAMS) 
  
        # extracting data in json format 
        data = r.json()
        signedUrlUpload = data['signedUrlUpload']
        print(signedUrlUpload)
        r = requests.put(signedUrlUpload, data=open(image, 'rb'))
        print(r.text)
        
if __name__ == "__main__":
    serviceEndpoint = 'https://0wqwlvpx17.execute-api.us-east-1.amazonaws.com/dev'
    integration(serviceEndpoint)