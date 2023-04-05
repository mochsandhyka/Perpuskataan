from ._base import db
from . import author,book,_base, borrowedBook, borrowedDetail,publisher,returnBook, returnDetail,user
import os
from pony.orm import db_session,commit
from app.models.user import User
from app.controllers.auth import hashPassword
from datetime import datetime
import uuid


db_params = {'provider': os.getenv('DB_PROVIDER'),
             'user': os.getenv('DB_USER'),
             'password': os.getenv('DB_PASSWORD'),
             'host': os.getenv('DB_HOST'),
             'database': os.getenv('DB_NAME')}


db.bind(**db_params)
db.generate_mapping(create_tables=True)

with db_session:
    try:
        User(idUser = str(uuid.uuid4()),username = "Admin",email = "Admin@adm.com", password = hashPassword("admin"),dateRegister = datetime.now(),role = "Admin" ,isActivate = True)
        commit()
    except:
        pass  
