import sys
from os import path
from argparse import ArgumentParser
import validate as Validate
from input import Input
from target import Target
from job import Job
from output import Output
from download import Download

def main():
    parser = ArgumentParser()
    parser.add_argument("-n", "--new", dest="new_job", help="Create new Backup Job (required)",
                        action='store_const', const=True)
    parser.add_argument("-d", "--download", dest="new_download", help="Download all files from S3 bucket (required)",
                        action='store_const', const=True)
    parser.add_argument("-f", "--config-file", dest="config_file", help="Alternate location of config.yaml file. (optional parameter defaults to ./config.yaml)",
                        action='store', type=str, required=False)

    results = parser.parse_args()

    # define path to config.yaml based on input
    CONFIG_PATH = results.config_file
    if results.config_file is None:
        CONFIG_PATH = './config.yaml'
    


    if results.new_job:
        print('New Job Starting ....')
        canLocateConfig, rawData = Validate.openFileYaml(CONFIG_PATH)
        if canLocateConfig:
            isValidated = Validate.validateSchema(CONFIG_PATH)
            if isValidated:
                # assign Input class to variable 
                inputDict = rawData['input']
                targetDict = rawData['target']
                jobDict = rawData['job']

                photoPath = inputDict['path']
                extensionTypeArray = inputDict['file-extensions']
                inputObject = Input(photoPath, extensionTypeArray)

                maxUploadNum = targetDict['max-uploaded-file']
                maxDownloadNum = targetDict['max-download-file']
                providerType = list(targetDict['provider'])[0]
                regionName = targetDict['provider'][providerType]['region']
                bucketName = targetDict['provider'][providerType]['bucket-name']
                storageClass = targetDict['provider'][providerType]['storage-class']
                targetObject = Target(maxUploadNum, maxDownloadNum, providerType, regionName, bucketName, storageClass)
                #new job object
                description = jobDict['job-description']
                cronTime = jobDict['runtime']['at']
                jobObjt = Job(description, cronTime, photoPath, inputObject, targetObject)

                #start new job
                jobObjt.createJob()  

    elif results.new_download:
        print('Starting new download...')
        canLocateConfig, rawData = Validate.openFileYaml(CONFIG_PATH)
        if canLocateConfig:
            isValidated = Validate.validateSchema(CONFIG_PATH)
            if isValidated:
                # assign Output class to variable
                outputDict = rawData['output']
                outputObjt = Output(outputDict['path'])
                targetDict = rawData['target']

                maxUploadNum = targetDict['max-uploaded-file']
                maxDownloadNum = targetDict['max-download-file']
                providerType = list(targetDict['provider'])[0]
                regionName = targetDict['provider'][providerType]['region']
                bucketName = targetDict['provider'][providerType]['bucket-name']
                storageClass = targetDict['provider'][providerType]['storage-class']
                targetObject = Target(maxUploadNum, maxDownloadNum, providerType, regionName, bucketName, storageClass)

                downloadObjct = Download(outputObjt.path, targetObject)
                downloadObjct.getFiles()
        
    else:
        print(parser.print_help())


if __name__=="__main__":
    main()