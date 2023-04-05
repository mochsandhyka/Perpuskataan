from flask import Flask
from flask_jwt_extended import JWTManager 
import os,uuid,re
from flask_cors import CORS
from pony.flask import Pony
from pony.orm import Database,db_session,commit
from .models._base import db
from datetime import datetime,timedelta
from flask_mail import Mail
from flasgger import Swagger,swag_from
from .config.swagger import template,swagger_config
import cloudinary


app = Flask(__name__)

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


 
#PONY
Pony(app)

#CORS
CORS(app)


#EMAIL REGEX
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]")

#MAIL
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = bool(os.getenv('MAIL_DEBUG'))
mail = Mail(app)


cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))


from app import routes
if __name__ == "__main__":
    app.run()
