class Input:
    def __init__(self, path, fileExtensions):
        if path is None:
            path = './photos'
        self.path = path
        self.fileExtensions = fileExtensions
