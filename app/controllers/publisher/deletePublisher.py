from flask_jwt_extended import jwt_required,get_jwt_identity
from app import responseHandler
from app.models.publisher import Publisher

@jwt_required(fresh=True)
def deletePublisher(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin" or currentUser['role'] == "User":    
            selectById = Publisher.get(idBookPublisher = id)
            if not selectById:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif selectById: 
                Publisher[id].delete()
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