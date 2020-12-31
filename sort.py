import os.path
from pathlib import Path
import json
import time

def openFileJSON(configPath):
    try:
        with open(configPath) as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError as exc:
        print('Unable to parse ', exc)
        return False, None
    return True, data

def getFilePaths(maxNum, photoPath, allowedExtArray, date):
    fileUploadArr = []
    maxFileIndex = 1
    #get all files sorted by newest creation date
    allFiles = sorted(Path(photoPath).iterdir(), key=os.path.getmtime)
    #reverse order of array 
    allFiles[::-1]
    # if not all files are being uploaded run all sort
    if maxNum is not None:
        if date is not None:
            for file in allFiles: 
                if not maxFileIndex <= maxNum:
                    break
                fileTime = os.path.getmtime(file)
                _, file_extension = os.path.splitext(file)
                if fileTime > date and file_extension in allowedExtArray:
                    fileUploadArr.append(file)
                    maxFileIndex += 1
        else:
            for file in allFiles:
                if not maxFileIndex <= maxNum:
                    break
                fileTime = os.path.getmtime(file)
                _, file_extension = os.path.splitext(file)
                if file_extension in allowedExtArray:
                    fileUploadArr.append(file)
                    maxFileIndex += 1

        return fileUploadArr
    else:
        # run sort based on all files 
        if date is not None:
            for file in allFiles:
                fileTime = os.path.getmtime(file)
                _, file_extension = os.path.splitext(file)
                if fileTime > date and file_extension in allowedExtArray:
                    fileUploadArr.append(file)
        else:
            for file in allFiles:
                _, file_extension = os.path.splitext(file)
                if file_extension in allowedExtArray:
                    fileUploadArr.append(file)

        return fileUploadArr


def sortFiles(photoPath, allowedExt, maxAllowedUpload):
    LAST_UPLOAD_PATH = './last-upload.json'

    canLocateConfig, rawData = openFileJSON(LAST_UPLOAD_PATH)
    if not canLocateConfig:
        print('Cannot Find last-upload file, starting upload from scratch')
        filePathsArray = getFilePaths(maxAllowedUpload, photoPath, allowedExt, None)
        return filePathsArray
    filePathsArray = getFilePaths(maxAllowedUpload, photoPath, allowedExt, rawData['upload-date'])
    return filePathsArray