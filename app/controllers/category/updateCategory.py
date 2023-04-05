from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,db,responseHandler,db,email_regex
from flask import request
from json_checker import Checker
from app.models.bookCategory import BookCategory

@jwt_required() 
def updateCategory(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":
            jsonBody = request.json
            data = requestMapping.Category(jsonBody)
            result = Checker(requestStruct.Category(),soft=True).validate(data)
            for key in requestStruct.Category():
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
            checkCategory = db.select(f"select category from tbl_book_category where category = '{result['category']}' and category != (select category from tbl_book_category where id_book_category = '{id}')")
            if checkCategory:
                response = {
                    "Message": "Category is Exist"
                }
                return responseHandler.badRequest(response)
            BookCategory[id].set(category = result['category'])
            response = {
                "Data": result,
                "Message": "Success Update Category"
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