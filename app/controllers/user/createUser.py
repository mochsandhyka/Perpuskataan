from app import requestMapping,requestStruct,responseHandler,email_regex,mail
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
from json_checker import Checker
from uuid import uuid4
from datetime import datetime
from pony.orm import select
from app.models.user import User
from app.controllers.mail import Message,sendEmail
from app.controllers.hashPassword import hashPassword

@jwt_required(fresh=True)
def createUser():
    try:
        currentUser = get_jwt_identity()
        if currentUser['role'] == "Admin":
            jsonBody = request.json
            data = requestMapping.createUser(jsonBody)
            result = Checker(requestStruct.createUser(),soft = True).validate(data)
            checkUser = select(a for a in User if a.username is result['username'] or a.email is result['email'])[:]
            if result['username'] == "" or result['password'] == "" or result['email'] == "":
                response = {
                    "Message": "All Data Must Be Filled"
                }
                return responseHandler.badRequest(response)
            elif checkUser:
                response = {
                    "Message": "Email or Password Already Registered"
                }
                return responseHandler.badRequest(response)
            elif not checkUser and email_regex.match(result['email']):
                idUser = str(uuid4())
                User(idUser = idUser, 
                     username = result['username'],
                     email = result['email'],
                     password = hashPassword(result['password']),
                     dateRegister = datetime.now(),
                     isActivate = False,
                     role = result['role'])
                
                # sendMail = sendEmail(result['email'], f"Activate Your Account Here : http://127.0.0.1:5000/activate/{idUser}", "Activate Your Account")
                # mail.send(sendMail)
                response = {
                    "Data": jsonBody,
                    "Message": "Check Your Email To Activate Your Account"
                }
                return responseHandler.ok(response)
            else:
                response = {
                    "Message": "Your Email is Not Valid"
                }
                return responseHandler.badRequest(response)
        if currentUser['role'] == "User":
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.forbidden(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)