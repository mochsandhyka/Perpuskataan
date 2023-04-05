from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,responseHandler,email_regex,mail
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
from json_checker import Checker
from uuid import uuid4
from datetime import datetime
from pony.orm import select
from app.models.publisher import Publisher

@jwt_required()
def createPublisher():
    currentUser = get_jwt_identity()
    try:
        #admin in deploy
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":
            jsonBody = request.json
            data = requestMapping.Publisher(jsonBody)
            result = Checker(requestStruct.Publisher(),soft=True).validate(data)
                
            #CHECK AUTHOR AND EMAIL IS EXIST OR NOT
            checkPublisher = select(a for a in Publisher if a.name is result['name'] or a.email is result['email']) 

            #CHECK RESULT IS NULL
            for key in requestStruct.Publisher():
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
            if checkPublisher:
                response ={ 
                    "Message": "Publisher or Email Already Registered"
                }
                return responseHandler.badRequest(response)
            elif email_regex.match(jsonBody['email']) :
                Publisher(idBookPublisher = uuid4(),
                           name = result['name'],
                           email = result['email'],
                           address = result['address'],
                           phoneNumber = result['phoneNumber'])
                response={
                    "Data": result,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
            elif not email_regex.match(jsonBody['email']):
                response={ 
                    "Message": "Email Not Valid"
                }
                return responseHandler.badRequest(response)
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