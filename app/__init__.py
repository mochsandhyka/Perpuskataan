from flask import Flask
from flask_jwt_extended import JWTManager 
import os,uuid,re
from flask_cors import CORS
from pony.flask import Pony
from pony.orm import Database
from .models._base import db
from datetime import datetime,timedelta
from flask_mail import Mail
from flasgger import Swagger,swag_from
from .config.swagger import template,swagger_config

app = Flask(__name__)

#MAIL
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '68ac9d019a7bc5'
app.config['MAIL_PASSWORD'] = 'f0b3886b327051'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

#JWT
JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT')



#UPLOAD
app.config['UPLOAD_FOLDER_BOOKS'] = os.getenv("UPLOAD_FOLDER_BOOKS")
app.config['UPLOAD_FOLDER_USERS'] = os.getenv("UPLOAD_FOLDER_USERS")
app.config['MAX_CONTENT_LENGHT'] = os.getenv("MAX_CONTENT_LENGHT")
app.config['ALLOWED_EXTENSIONS'] = os.getenv("ALLOWED_EXTENSION")
allowedextensions = app.config['ALLOWED_EXTENSIONS']
uploadFolderBooks = app.config['UPLOAD_FOLDER_BOOKS']
uploadFolderUsers = app.config['UPLOAD_FOLDER_USERS']


#SWAGGER
SWAGGER = {
    'title': "PERPUSKATAAN API",
    'uiversion': 3
}
a = Swagger(app,config=swagger_config,template=template)
 
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
