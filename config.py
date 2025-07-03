import os

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or "b'\xaa\x08\xca\x9c=\xab\xb6\x8cJ5wx3H\r\x13'"

    MONGODB_SETTINGS={'db':'UTA_Enrollment'}