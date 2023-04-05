from flask_jwt_extended import jwt_required
from app.models.user import User
from app import responseHandler

@jwt_required()
def readUser(id):                     
    try:
        readById = User.get(idUser = id)
        data = readById.to_dict()
        response = {
            "Data": data
        } 
        return responseHandler.ok(response)
    except Exception as err:
            response = {
                "Message": "User Not Found"
            }
            return responseHandler.badRequest(response)