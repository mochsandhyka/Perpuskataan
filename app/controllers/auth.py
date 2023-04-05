from app.models.user import User
from app import responseHandler
from flask import request,jsonify
from flask_jwt_extended import create_refresh_token,create_access_token
from pony.orm import select
import hashlib,os

def hashPassword(password):
    hashpassword = hashlib.md5((password+os.getenv("SALT_PASSWORD")).encode()).hexdigest()
    return hashpassword

def login():
    try:
        jsonBody = request.json
        hashPass = hashPassword(jsonBody['password'])
        user = select(a for a in User if a.username is jsonBody['username'] and a.password is hashPass)[:]
        if not user:
            response = {
                "Message": "Invalid Username / Password "
            }
            return responseHandler.badRequest(response)
        elif user:
            currentUser = user[0].to_dict()
            if currentUser['isActivate'] == False or currentUser['isActivate'] == True:
                accessToken = create_access_token(identity=currentUser,fresh=True)
                refreshToken = create_refresh_token(identity=accessToken)
                response = jsonify({
                    "accessToken": accessToken,
                    "refreshToken": refreshToken,
                    "Message": "Login Success"
                })
                return response
            elif currentUser['isActivate'] == False:
                response = {
                    "Message": "Please Check Email to Activate Your Account"
                }
                return responseHandler.badRequest(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    