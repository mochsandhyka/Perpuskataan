from app.models import db
from app import requestMapping,requestStruct,responseHandler,allowedextensions,uploadFolderBooks
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
import os

def listBooks():
    try:
        listBooks = db.select(f"select a.id_book,a.stock,a.book_title,a.id_book_category,a.id_book_author,a.id_book_publisher,a.picture,b.category,c.name,c.email,c.gender,c.address,c.phone_number,d.name,d.email,d.address,d.phone_number from tbl_book as a left join tbl_book_category as b on(a.id_book_category = b.id_book_category) left join tbl_book_author as c on(a.id_book_author = c.id_book_author) left join tbl_book_publisher as d on (a.id_book_publisher = d.id_book_publisher)")
        data = []
        for i in listBooks:
            data.append({
                "idBook": i[0],
                "stock": i[1],
                "bookTitle": i[2],
                "idBookCategory": i[3],
                "idBookAuthor": i[4],
                "idBookPublisher": i[5],
                "picture": i[6],
                "category": i[7],
                "authorName": i[8],
                "authorEmail": i[9],
                "authorGender": i[10],
                "authorAddress": i[11],
                "authorPhoneNumber": i[12],
                "publisherName": i[13],
                "publisherEmail": i[14],
                "publisherAddress": i[15],
                "publisherPhoneNumber": i[16]
            })
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)