from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,db,responseHandler,db,email_regex
from flask import request
from json_checker import Checker
from app.models.author import BookAuthor

@jwt_required() 
def updateAuthor(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":
            jsonBody = request.json
            data = requestMapping.Authors(jsonBody)
            result = Checker(requestStruct.Authors(),soft=True).validate(data)
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
            checkName = db.select(f"select name from tbl_book_author where name = '{result['name']}' and name != (select name from tbl_book_author where id_book_author =    '{id}')")
            if checkName:
                response = {
                    "Message": "Author Name is Exist"
                }
                return responseHandler.badRequest(response)
            checkEmail = db.select(f"select email from tbl_book_author where email = '{result['email']}' and email != (select email from tbl_book_author where id_book_author = '{id}')")
            if checkEmail:
                response = {
                    "Message": "Email is exist"
                }
                return responseHandler.badRequest(response)
            BookAuthor[id].set(name = result['name'],
                           email = result['email'],
                           gender = result['gender'],
                           address = result['address'],
                           phoneNumber = result['phoneNumber'])
            response = {
                "Data": result,
                "Message": "Success Update Author"
            }
            return responseHandler.ok(response)
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