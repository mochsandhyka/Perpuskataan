from app.models import db
from app import requestMapping,requestStruct,responseHandler,allowedextensions,uploadFolderBooks
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
import os

def deleteBook(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            selectById = (f"select id_book from tbl_book where id_book = '{id}'")
            data = []
            for i in db.execute(selectById):
                data.append({
                    "idBook": i[0]
                }) 
            if not data:
                response ={
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_book where id_book = '{id}'")
                db.execute(deleteById)
                response = {
                    "Message": "Delete Success"
                }
                return responseHandler.ok(response)
            response = {
                "Message": "Delete Invalid"
            }
            return responseHandler.badRequest(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response = {
            "Error": str(err)
            }
            return responseHandler.badGateway(response)   
    