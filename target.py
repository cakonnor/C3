class Target:
    def __init__(self, maxUploadNum, maxDownloadNum, provider, region, bucketName, storageClass):
        self.maxUploadNum = maxUploadNum
        self.maxDownloadNum = maxDownloadNum
        self.provider = provider
        self.region = region
        self.bucketName = bucketName
        self.storageClass =  storageClass