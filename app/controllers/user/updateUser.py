from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,db,responseHandler,db,email_regex
from flask import request
from json_checker import Checker
import os,cloudinary 
from app.models.user import User
from app.controllers.hashPassword import hashPassword
from cloudinary import uploader


@jwt_required()
def updateUser(id):
    currentUser = get_jwt_identity()
    if currentUser['idUser'] == id:
        uploadFile = request.files['picture']
        data = requestMapping.userUpdate(request.form)
        result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
        success = False
        try:
            # a = select(a for a in User if str(a.idUser) is currentUser['idUser'])[:]
            # print(a[0].idUser)
            # check = User.get(username = result['username'] and select(), email = result['email'] and select(a for a in User if str(a.idUser) != currentUser['idUser']))
            # print(check)
            if currentUser["username"] != result["username"]:
                checkUsername = db.select(f"select username from tbl_user where username = '{result['username']}' and username != (select username from tbl_user where id_user = '{currentUser['idUser']}')")
                if checkUsername:
                    response = {
                        "Message": "User is exist"
                    }
                    return responseHandler.badRequest(response)
            if currentUser["email"] != result["email"]:
                checkEmail = db.select(f"select email from tbl_user where email = '{result['email']}' and email != (select email from tbl_user where id_user = '{currentUser['idUser']}')")
                if checkEmail:
                    response = {
                        "Message": "Email is exist"
                    }
                    return responseHandler.badRequest(response)
            if result['username'] =="" or result['email'] =="" or result['password'] =="" or result['name'] =="" or result['gender'] =="" or result['address'] == "" or result['city'] =="" or result['phoneNumber'] =="":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if email_regex.match(result['email']):
                #user = select(a for a in User if str(a.idUser) is currentUser['idUser'])[:]
                cloudinary.uploader.upload(uploadFile,
                                               folder = "profiles/",
                                               public_id = "profile"+"_"+currentUser['idUser'],
                                               overwrite = True,
                                               width = 250,
                                               height = 250,
                                               grafity = "auto",
                                               radius = "max"
                                               )
                success = True
                if success:
                        result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
                        picture = "profile"+"_"+currentUser['idUser']
                        User[id].set(username = result['username'],
                                     email = result['email'], 
                                     password = hashPassword(result['password']), 
                                     name = result['name'], gender = result['gender'], 
                                     address = result['address'], 
                                     city = result['city'],
                                     phoneNumber = result['phoneNumber'],
                                     picture = picture)
                        result.update({
                             "picture": picture
                        })
                        response = {
                            "Data": result,
                            "Message": "Success Update User"
                        }
                        return responseHandler.ok(response)
                elif not success:
                        response = { 
                            "Message": "File is not Valid"
                        }
                        return responseHandler.badRequest(response)
            response = {
                "Message": "Email not Valid"
            }
            return responseHandler.badRequest(response)
        except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)