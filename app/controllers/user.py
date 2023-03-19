from app.models import db
from app import requestMapping,requestStruct,responseHandler,email_regex,os
from flask import request
from json_checker import Checker
from uuid import uuid4
import hashlib
from flask_jwt_extended import jwt_required,get_jwt_identity

def listUsers():
    try:
        listUsers = db.select(f"select id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role from tbl_user")
        data = []
        for i in listUsers:
            data.append({
                "idUser": i[0],
                "username": i[1],
                "email": i[2],
                "password": i[3],
                "name": i[4],
                "gender": i[5],
                "address": i[6],
                "city": i[7],
                "phoneNumber":i[8],
                "dateRegister":i[9],
                "picture": i[10],
                "role": i[11]
            })
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required(fresh=True)
def createUser():
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "Admin":
        try:
            jsonBody = request.json
            data = requestMapping.User(jsonBody)
            result = Checker(requestStruct.User(),soft=True).validate(data)
            checkUser = db.select(f"select *from tbl_user where username = '{jsonBody['username']}' or email = '{jsonBody['email']}'")

            if jsonBody['username'] =="" or jsonBody['email'] =="" or jsonBody['password'] =="" or jsonBody['name'] =="" or jsonBody['gender'] =="" or jsonBody['address'] == "" or jsonBody['city'] =="" or jsonBody['phoneNumber'] =="" or jsonBody['role'] =="":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkUser:
                response = {
                    "Message": (f" Username : '{jsonBody['username']}' or Email : '{jsonBody['email']}' is Exist ")
                }
                return responseHandler.badRequest(response)
            else:
                password = result['password']
                hashpassword = hashlib.md5((password+ os.getenv("SALT_PASSWORD")).encode())
                createUser = (f"insert into tbl_user(id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role) values('{str(uuid4())}','{result['username']}','{result['email']}','{hashpassword.hexdigest()}','{result['name']}','{result['gender']}','{result['address']}','{result['city']}','{result['phoneNumber']}',now(),'{'a.jpg'}','{result['role']}')")
                db.execute(createUser)
                response = {
                    "Data": jsonBody,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
        except Exception as err:
            response ={
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)

@jwt_required()
def readUser(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            get_jwt_identity()
            readById = db.select(f"select id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role from tbl_user where id_user = '{id}'" )
            data = []
            for i in readById:
                data.append({
                    "idUser": i[0],
                    "username":i[1],
                    "email": i[2],
                    "password": i[3],
                    "name": i[4],
                    "gender": i[5],
                    "address": i[6],
                    "city": i[7],
                    "phoneNumber":i[8],
                    "dateRegister":i[9],
                    "picture":i[10],
                    "role":i[11]
                })
            if not data:
                    response = {
                        "Message": "Book Not Found"
                    }
                    return responseHandler.badRequest(response)
            response ={
                    "Data": data[0]
                }
            return responseHandler.ok(response)
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

@jwt_required()
def updateUser(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            jsonBody = request.json
            data = requestMapping.User(jsonBody)
            hashpass = hashlib.md5((jsonBody['password']+os.getenv("SALT_PASSWORD")).encode())
            updateUser = (f"update tbl_user set username='{data['username']}' ,password = '{hashpass.hexdigest()}',email='{data['email']}',name='{data['name']}',gender='{data['gender']}',address='{jsonBody['address']}',city='{data['city']}',phone_number='{data['phoneNumber']}' where id_user = '{id}'")
            db.execute(updateUser)
            response = {
                "Data": updateUser,
                "Message": "Success Update User"
            }
            return responseHandler.ok(response)
        except Exception as err:
            response = {
                "Message": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)
    

@jwt_required()
def deleteUser(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            selectById = (f"select id_user from tbl_user where id_user = '{id}'")
            data = []
            for i in db.execute(selectById):
                dictData = {
                    "idUser": i[0]
                }
                data.append(dictData)
            if not data:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_user where id_user = '{id}'")
                db.execute(deleteById)
                response = {
                    "Message": "Delete Success"
                }
                return responseHandler.ok(response)
            response = {
                "Message": "Delete Invalid"
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
