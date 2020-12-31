import boto3
import botocore

class Download:
    def __init__(self, downloadPath, targetObjct):
        self.downloadPath = downloadPath
        self.targetObjct = targetObjct

    def getFiles(self):
        print('Downloading files from S3....')
        client = boto3.client('s3', region_name=self.targetObjct.region)
        listObjt = []
        maxFileIndex = 1
        maxNum = self.targetObjct.maxDownloadNum

        # get all files from s3
        for objt in client.list_objects(Bucket=self.targetObjct.bucketName)['Contents']:
            listObjt.append(objt['Key'])
        if listObjt:
            
            for file in listObjt:
                if maxNum is not None:
                    if not maxFileIndex <= maxNum:
                        break
                filePath = self.downloadPath + '/' + file
                try: 
                    res = client.download_file(
                        Filename = filePath, 
                        Bucket = self.targetObjct.bucketName, 
                        Key = file
                    )
                    print('Downloaded file:', file, 'successfuly')
                    maxFileIndex+= 1
                except botocore.exceptions.ClientError as error:
                    raise error


        else:
            print('Unable to find any objects in bucket, stopping download ..')

