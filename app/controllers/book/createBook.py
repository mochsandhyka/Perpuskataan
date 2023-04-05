from flask_jwt_extended import jwt_required,get_jwt_identity
from app import requestMapping,requestStruct,responseHandler,email_regex,mail,db,allowedextensions,os,uploadFolderBooks
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
from json_checker import Checker
from uuid import uuid4
from datetime import datetime
from pony.orm import select
from app.models.book import Book

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedextensions

@jwt_required()    
def createBook():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":
            files = request.files.getlist('picture')
            jsonBody = request.form
            data = requestMapping.Books(jsonBody)
            result = Checker(requestStruct.Books(),soft=True).validate(data)
            checkBook = db.select(f"select *from tbl_book where book_title = '{result['bookTitle']}' and id_book_author = '{result['bookAuthor']}'")

            if result['stock'] == "" or result['bookTitle'] == "" or result['bookCategory'] == "" or result['bookAuthor'] == "" or result['bookPublisher'] == "":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkBook:
                response = {
                    "Message": (f" Book '{jsonBody['bookTitle']}' is Exist ")
                }
                return responseHandler.badRequest(response)
            else:
                for i in files:
                    if i and allowed_file(i.filename):
                        filename = secure_filename(i.filename)
                        picfilename = str(uuid4()) + '_' + filename 
                        i.save(os.path.join(uploadFolderBooks,picfilename))
                        success = True
                    if success:
                        createBook = (f"insert into tbl_book(id_book,stock,book_title,id_book_category,id_book_author,id_book_publisher,picture) values ('{str(uuid4())}','{jsonBody['stock']}','{result['bookTitle']}','{result['bookCategory']}','{result['bookAuthor']}','{result['bookPublisher']}','{picfilename}')")
                        db.execute(createBook)
                        response = {
                            "Data": jsonBody,
                            "Message": "Data Created"
                        }
                        return responseHandler.ok(response)
                if not files:
                    picfilename = "book.jpg"
                    createBook = (f"insert into tbl_book(id_book,stock,book_title,id_book_category,id_book_author,id_book_publisher,picture) values ('{str(uuid4())}',{jsonBody['stock']},'{result['bookTitle']}','{result['bookCategory']}','{result['bookAuthor']}','{result['bookPublisher']}','{picfilename}')")
                    db.execute(createBook)
                    response={
                                "Data": createBook,
                                "Message": "Data Created"
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
    

def read():
    try:
        a = db.select(f"select id_book_author,name from tbl_book_author")
        b = db.select(f"select id_book_category,category from tbl_book_category")
        c = db.select(f"select id_book_publisher,name from tbl_book_publisher")
        data = []
        for i in a:
            data.append({
                "idBookAuthor": i[0],
                "nameAuthor": i[1]
            })
        data2 = []
        for i in b:
            data2.append({
                "idBookCategory": i[0],
                "category": i[1]
            })
        data3 = []
        for i in c:
            data3.append({
                "idBookPublisher": i[0],
                "namePublisher": i[1]
            })
        response = {
            "Author": data,
            "Category": data2,
            "Publisher": data3
        }
        return responseHandler.ok(response)
    except Exception as err:
        pass