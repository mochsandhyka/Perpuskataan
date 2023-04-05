from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,responseHandler,email_regex,mail
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
from json_checker import Checker
from uuid import uuid4
from datetime import datetime
from pony.orm import select
from app.models.bookCategory import BookCategory


@jwt_required()
def createCategory():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":
            jsonBody = request.json
            data = requestMapping.Category(jsonBody)
            result = Checker(requestStruct.Category(),soft=True).validate(data)
            checkBookCategory = select(a for a in BookCategory if a.category is result['category'])
            for key in requestStruct.Authors():
                if key not in jsonBody:
                    response = {
                        "Message": f"{key} is not in Form Request"
                    }
                    return responseHandler.badRequest(response)
                elif key == "":
                    response = {
                        "Message": f"Form {key} Must be Filled"
                    }
                    return responseHandler.badRequest(response)
            if checkBookCategory:
                response ={ 
                    "Message": "Category Already Registered"
                }
                return responseHandler.badRequest(response)
            else:
                BookCategory(idBookCategory = str(uuid4()),
                             category = result['category'])
                response = {
                    "Data": result,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response ={
                "Error": str(err)
            }
            return responseHandler.badGateway(response)    