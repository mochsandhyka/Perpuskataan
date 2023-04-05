from flask_jwt_extended import jwt_required,get_jwt_identity
from app import responseHandler
from app.models.author import BookAuthor
import cloudinary
from cloudinary import uploader

@jwt_required(fresh=True)
def deleteAuthor(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":    
            selectById = BookAuthor.get(idBookAuthor = id)
            if not selectById:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif selectById: 
                BookAuthor[id].delete()
                response = {
                    "Message": "Delete Success"
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