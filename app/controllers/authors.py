from app.models import db
from app import responseHandler,requestStruct,requestMapping,email_regex
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity


def listAuthors():
    try:
        listBookAuthor = db.select(f"select id_book_author,name,email,gender,address,phone_number from tbl_book_author")
        data = []
        for i in listBookAuthor:
            data.append({
                "id": i[0],
                "name": i[1],
                "email": i[2],
                "gender": i[3],
                "address": i[4],
                "phoneNumber": i[5]
            })
        return responseHandler.ok(data)   
    except Exception as err:
        response = {
            "Error": str(err)
            }
        return responseHandler.badRequest(response)
   
@jwt_required()
def createAuthor():
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        jsonBody = request.json
        data = requestMapping.Authors(jsonBody)
        try:
            result = Checker(requestStruct.Authors(),soft=True).validate(data)
            checkBookAuthor = db.select(f"select * from tbl_book_author where name = '{jsonBody['name']}'")
            if jsonBody['name'] == "" or jsonBody['email'] == "" or jsonBody['gender'] == "" or jsonBody['address'] == "" or jsonBody['phoneNumber'] == ""  :
                response ={
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkBookAuthor:
                response ={ 
                    "Message": "Author Already Registered"
                }
                return responseHandler.badRequest(response)
            elif not checkBookAuthor and email_regex.match(jsonBody['email']) :
                createBookAuthor = (f"insert into tbl_book_author(id_book_author,name,email,gender,address,phone_number) values('{str(uuid4())}','{result['name']}','{result['email']}','{result['gender']}','{result['address']}','{result['phoneNumber']}')")
                db.execute(createBookAuthor)
                response={
                    "Data": jsonBody,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
            elif not email_regex.match(jsonBody['email']):
                response={ 
                    "Message": "Email Not Valid"
                }
                return responseHandler.badRequest(response)
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
    
def readAuthor(id):
    try:
        updateAuthorById = db.select(f"select id_book_author,name,email,gender,address,phone_number from tbl_book_author where id_book_author = '{id}'")
        data = []
        for i in updateAuthorById:
            data.append({
                "idBookAuthor": i[0],
                "name": i[1],
                "email": i[2],
                "gender": i[3],
                "address": i[4],
                "phoneNumber": i[5]
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
def updateAuthor(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            jsonBody = request.json
            data = requestMapping.Authors(jsonBody)
            updateBookAuthor = (f"update tbl_book_author set name='{data['name']}', email='{data['email']}',gender='{data['gender']}',address='{data['address']}',phone_number='{data['phoneNumber']}' where id_book_author = '{id}'")
            db.execute(updateBookAuthor)
            response = {
                "Data": updateBookAuthor,
                "Message": "Success Update Author"
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
def deleteAuthor(id):
    currentUser = get_jwt_identity()
    role = currentUser['role']
    if role == "admin":
        try:
            selectById = (f"select id_book_author from tbl_book_author where id_book_author = '{id}'")
            data=[]
            for i in db.execute(selectById):
                dictData = {
                    "id_book_author": i[0]
                }
                data.append(dictData)
            if not data:
                response = {
                    "message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_book_author where id_book_author = '{id}'")
                db.execute(deleteById) 
                response = { 
                    "Message": "Delete Success"
                } 
                return responseHandler.ok(response)
            else:
                response = { 
                    "Message": "Delete invalid"
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

