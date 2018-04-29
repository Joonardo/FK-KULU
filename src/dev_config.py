SECRET = "very secret key"
DEBUG = False

LOG_FILE = "log"
LOG_FORMAT = '''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''

SENDGRID_APIKEY = "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"

RECEIPTS_FOLDER = '/tmp/'
TMP_FOLDER = '/tmp/'

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
