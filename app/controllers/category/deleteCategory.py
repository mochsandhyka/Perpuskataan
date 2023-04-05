from flask_jwt_extended import jwt_required,get_jwt_identity
from app import responseHandler
from app.models.bookCategory import BookCategory


@jwt_required(fresh=True)
def deleteCategory(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":    
            selectById = BookCategory.get(idBookCategory = id)
            if not selectById:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif selectById: 
                BookCategory[id].delete()
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