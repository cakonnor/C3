import boto3
import botocore
import json
import time
import os.path
from pathlib import Path
import sys

LAST_UPLOAD_PATH = './last-upload.json'

def uploadFiles(fileList, region, bucketName, storageClass):
    client = boto3.client('s3', region_name=region)
    lastFileCreateDate = ''
    if fileList:
        for file in fileList:
            '''
            try:
                res = client.upload_file(
                    Filename = str(file), 
                    Bucket = bucketName, 
                    Key = os.path.basename(file),
                    ExtraArgs = {
                    'StorageClass': storageClass
                    }
                )
                print('Uploaded file:', file, 'successfuly')
                lastFileCreateDate = os.path.getmtime(file)
            except botocore.exceptions.ClientError as error:
                raise error
'''
            lastFileCreateDate = os.path.getmtime(file)
        # update or create last upload json file
        createJSON(LAST_UPLOAD_PATH, lastFileCreateDate)

    else:
        print('No new Files to Upload, skipping upload session')

def createJSON(fileName, date):
    
    data = {"upload-date":date}

    try:
        with open(fileName, 'w', encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, ensure_ascii=False, indent=4)
    except ValueError as exc:
        print('Unable to write last Upload File ', exc)

    

    
