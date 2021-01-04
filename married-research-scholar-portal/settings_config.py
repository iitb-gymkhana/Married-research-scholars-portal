import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "SECRET"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATIC_URL = "/static/"
MEDIA_URL = "/upload/"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "gymkhana.iitb.ac.in"]

# Email server settings
EMAIL_HOST = "smtp-auth.iitb.ac.in"
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 25
# EMAIL_PORT = 587

EMAIL_HOST_USER = "180070032@iitb.ac.in" # use the appropriate sender email id

EMAIL_HOST_PASSWORD = "00b708055791c425d0bac143bf930cfe"  # use the appropriate sender email password
# Email Id which will appear in From header in email
EMAIL_FROM = "180070032@iitb.ac.in"

EMAIL_BACKEND = "core.notification.IITBEmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_MAIL = EMAIL_HOST_USER
SERVER_EMAIL = "180070032@iitb.ac.in"
EMAIL_SUBJECT_PREFIX = "[Married scholars portal]"

ADMINS = (("Nautatva Navlakha", "nnautatva@gmail.com"),("Ipsit Mantri", "mmkipsit@gmail.com"))

# DATABASES
# Define databases here to override default Databases.
DATABASES = {
    'development': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MRSP',
        'USER': 'ipsit',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MRSP',
        'USER': 'ipsit',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    },
}

# OAuth2 settings
AUTHORIZATION_URL = "https://gymkhana.iitb.ac.in/sso/oauth/authorize/"
REDIRECT_URI = "https://gymkhana.iitb.ac.in/mrsp/oauth/callback/"
CLIENT_ID = "QYeB9w4SSXCxQi2hNiaqJ1P1cZPeXpqOBcKNsTPe"
# CLIENT_ID = "ohRIIM0R1kEIxHOu67RgAvp3i2HkGEyYteQ40N1b"
CLIENT_SECRET = "ym4wqwvzUpKYYJVZ4gIVw2grfKZawJpJpr64RbOTdIttlroru8Ritpe1qbY9Wc7Pdsv3AFOTEqWYnB2wPQ2i3Qyv79d6GTPwSvWXcuZOk14WNI3tlj8i9PXpKqe9RZpw"
# CLIENT_SECRET = "9EU9GyaGNyuFh36Hqdv2mhN2bTgSoX6wPxCOHSt85F33a8qBZ6xDXkMcg6GWjXoAijgVOW0UFqfg2HR8JFAlNy6mCYOJHVsKbZzIQIH8jIlJYT3LaFjMaev9A8prulMR"
SCOPE = "profile%20ldap%20insti_address%20insti_address%20program"
SSO_TOKEN_URL = "https://gymkhana.iitb.ac.in/sso/oauth/token/"
# GRANT_TYPE = "authorization_code"
SSO_PROFILE_URL = "https://gymkhana.iitb.ac.in/sso/user/api/user/?fields=first_name,last_name,roll_number,insti_address"
