from flask import Flask
from flask_jwt_extended import JWTManager 
import os,uuid,re
from flask_cors import CORS
from pony.flask import Pony
from pony.orm import Database
from .models._base import db

app = Flask(__name__)

#JWT
JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
#app.config['JWT_TOKEN_LOCATION'] = os.getenv('JWT_TOKEN_LOCATION')
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT')
#app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = os.getenv('JWT_ACCESS_CSRF_HEADER_NAME')
app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "csrftoken"
app.config['JWT_COOKIE_CSRF_PROTECT'] = True


#UPLOAD
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
app.config['MAX_CONTENT_LENGHT'] = os.getenv("MAX_CONTENT_LENGHT")
app.config['ALLOWED_EXTENSIONS'] = os.getenv("ALLOWED_EXTENSION")
allowedextensions = app.config['ALLOWED_EXTENSIONS']
uploadfolder = app.config['UPLOAD_FOLDER']


#DB
db__params = {'provider': os.getenv('DB_PROVIDER'),
             'user': os.getenv('DB_USER'),
             'password': os.getenv('DB_PASSWORD'),
             'host': os.getenv('DB_HOST'),
             'database': os.getenv('DB_NAME')}

#PONY
Pony(app)

#CORS
CORS(app)

#GENERATE ID
def generateId():
    myId = uuid.uuid4
    return myId

#EMAIL REGEX
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]")





from app import routes
if __name__ == "__main__":
    app.run()
