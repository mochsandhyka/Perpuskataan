from app.models import db
from app import requestMapping,requestStruct,responseHandler,allowedextensions,uploadFolderBooks
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
import os

@jwt_required() 
def updateBook(id):
    currentUser = get_jwt_identity()
    if currentUser['role'] == "Admin":
        try:
            jsonBody = request.json
            data = requestMapping.Books(jsonBody)
            result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
            checkBook = db.select(f"select book_title from tbl_book where book_title = '{result['bookTitle']}' and book_title != (select book_title from tbl_book where id_book = '{id}')")
            if checkBook:
                response = {
                    "Message": "Book is Exist"
                }
                return responseHandler.badRequest(response)
            else:
                updateBook = (f"update tbl_book set stock = '{result['stock']}', book_title = '{result['bookTitle']}', id_book_category = '{result['bookCategory']}', id_book_author = '{result['bookAuthor']}', id_book_publisher = '{result['bookPublisher']}' where id_book = '{id}'")
                db.execute(updateBook)
                response = {
                    "Data": updateBook,
                    "Message": "Successs Update Book"
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
