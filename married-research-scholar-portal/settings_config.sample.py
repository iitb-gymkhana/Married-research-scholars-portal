import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "SECRET"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATIC_URL = "/static/"
MEDIA_URL = "/upload/"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATABASES
# Define databases here to override default Databases.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

# Email server settings
EMAIL_HOST = "smtp-auth.iitb.ac.in"
EMAIL_PORT = 25

EMAIL_HOST_USER = ""

EMAIL_HOST_PASSWORD = ""

# Email Id which will appear in From header in email
EMAIL_FROM = ""

# EMAIL_BACKEND = "core.notification.IITBEmailBackend"

SERVER_EMAIL = ""

EMAIL_SUBJECT_PREFIX = "[Married scholars portal]"

ADMINS = (("Nautatva Navlakha", "nnautatva@gmail.com"),)

# DATABASES
# Define databases here to override default Databases.
DATABASES = {
    "development": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# OAuth2 settings
AUTHORIZATION_URL = "https://gymkhana.iitb.ac.in/sso/oauth/authorize/"
REDIRECT_URI = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
SCOPE = "profile%20ldap%20insti_address%20insti_address%20program"
SSO_TOKEN_URL = "https://gymkhana.iitb.ac.in/sso/oauth/token/"
# GRANT_TYPE = "authorization_code"
SSO_PROFILE_URL = "https://gymkhana.iitb.ac.in/sso/user/api/user/?fields=first_name,last_name,roll_number,insti_address"
