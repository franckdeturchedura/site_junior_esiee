import os
cd = os.getcwd()
class Config(object):
    DEBUG = True
    MAX_CONTENT_LENGTH =  16 * 1024 * 1024
    UPLOAD_FOLDER = os.getcwd()+'/upload/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
