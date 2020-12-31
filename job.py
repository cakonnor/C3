import schedule
import time

import upload as Upload
import sort as Sort

class Job:
    def __init__(self, description, cronTime, photoPath, inputObjt, targetObjt):
        self.description = description
        self.cronTime = cronTime
        self.photoPath = photoPath
        self.inputObjt = inputObjt
        self.targetObjt = targetObjt

    def createJob(self):
        print('Creating Cron Job ...')
        #convert time to 24hr format
        secVal = "{0:0=2d}".format(self.cronTime[0]['second'])
        minVal =  "{0:0=2d}".format(self.cronTime[1]['minute'])
        hourVal =  "{0:0=2d}".format(self.cronTime[2]['hour'])
        fullTime = "%s:%s:%s" % (secVal, minVal, hourVal)

        #get list of files
        fileArray = Sort.sortFiles(self.photoPath, self.inputObjt.fileExtensions, self.targetObjt.maxUploadNum)

        schedule.every().day.at(fullTime).do(Upload.uploadFiles, fileArray, self.targetObjt.region, self.targetObjt.bucketName, self.targetObjt.storageClass)
        Upload.uploadFiles(fileArray, self.targetObjt.region, self.targetObjt.bucketName, self.targetObjt.storageClass)
'''
        while True:
            schedule.run_pending()
'''


        

        