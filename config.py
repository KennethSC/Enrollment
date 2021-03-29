import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'i\xba\xf7\x91|\xff\x03\xc8\xf2\xa1I\x0e\xb9\xb2\xa7\x1b'

    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment'
    }