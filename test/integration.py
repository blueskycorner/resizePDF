import sys
import os
from buildSignedUrlUpload import buildSignedUrlUpload
# import resizePDF
import requests
import uuid

buildSignedUrlUpload_URLParamName = 'buildSignedUrlUpload_URL'
resizePDF_URLParamName = 'resizePDF_URL'
imagesList = ["test/Data/2016-06_Alex_CP_Bulletin1ertrim-page1.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page2.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page3.jpg"]
print (sys.path)
def integration():
    buildSignedUrlUpload_URL = os.getenv(buildSignedUrlUpload_URLParamName)
    resizePDF_URL = os.getenv(resizePDF_URLParamName)
    
    # for image in imagesList:
    #     id = uuid.uuid4()
    #     path, filename = os.path.split(image)
    #     PARAMS = {'prefix':id, 'filename': filename} 
    #     r = requests.get(url = buildSignedUrlUpload_URL, params = PARAMS) 
  
    #     # extracting data in json format 
    #     data = r.json() 
    #     print(data)