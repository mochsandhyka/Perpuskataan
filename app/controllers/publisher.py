from app.models import db
from app import requestMapping,requestStruct,responseHandler,email_regex
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity

def listPublisher():
    try:
        listPublisher = db.select(f"select id_book_publisher,name,email,address,phone_number from tbl_book_publisher")
        data = []
        for i in listPublisher:
            data.append({
                "id": i[0],
                "name": i[1],
                "email": i[2],
                "address": i[3],
                "phoneNumber": i[4]
            })
        return responseHandler.ok(data)
    except Exception as err:
        response={
            "Message": str(err)
        }
        return responseHandler.badGateway(response)

@jwt_required()
def createPublisher():
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            jsonBody = request.json
            data = requestMapping.Publisher(jsonBody)
            result = Checker(requestStruct.Publisher(),soft=True).validate(data)
            checkBookPublisher = db.select(f"select * from tbl_book_publisher where name = '{jsonBody['name']}'")
            if jsonBody['name'] == "" or jsonBody['email'] == "" or jsonBody['address'] == "" or jsonBody['phoneNumber'] == "":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkBookPublisher:
                response ={
                    "Message": "Publisher Already Registered"
                }
                return responseHandler.badRequest(response)
            elif not checkBookPublisher and email_regex.match(jsonBody['email']):
                createBookPublisher = (f"insert into tbl_book_publisher(id_book_publisher,name,email,address,phone_number) values('{str(uuid4())}','{result['name']}','{result['email']}','{result['address']}','{result['phoneNumber']}')")
                db.execute(createBookPublisher)
                response = {
                    "Data": jsonBody,
                    "Message": "Data Created"
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
    
    
def readPublisher(id):
    try:
        readById = db.select(f"select id_book_publisher,name,email,address,phone_number from tbl_book_publisher where id_book_publisher = '{id}'")
        data = []
        for i in readById:
            data.append({
                "idBookPublisher": i[0],
                "name": i[1],
                "email": i[2],
                "address": i[3],
                "phoneNumber": i[4]
            })
        if not data:
            response = {
                "Message": "No Data Found"
            }
            return responseHandler.badGateway(response)
        response = {
            "Data": data[0]
        }
        return responseHandler.ok(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)

@jwt_required() 
def updatePublisher(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            jsonBody = request.json
            data = requestMapping.Publisher(jsonBody)
            updateBookPublisher = (f"update tbl_book_publisher set name='{data['name']}', email='{data['email']}',address='{data['address']}',phone_number='{data['phoneNumber']}' where id_book_publisher = '{id}'")
            db.execute(updateBookPublisher)
            response = {
                "Data": updateBookPublisher,
                "Message": "Success Update Publisher"
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
def deletePublisher(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            selectById = (f"select id_book_publisher from tbl_book_publisher where id_book_publisher = '{id}'")
            data=[]
            for i in db.execute(selectById):
                dictData = {
                    "idBookPublisher": i[0]
                }
                data.append(dictData)
            if not data:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_book_publisher where id_book_publisher = '{id}'")
                db.execute(deleteById) 
                response = { 
                    "Message": "Delete Success"
                } 
                return responseHandler.ok(response)
            else:
                response = { 
                    "Message": "Delete Invalid"
                } 
                return responseHandler.badRequest(response)
        except Exception as err:
            response={
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)