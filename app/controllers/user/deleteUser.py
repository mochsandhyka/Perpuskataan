from flask_jwt_extended import jwt_required,get_jwt_identity
from app import responseHandler
from app.models.user import User
import cloudinary
from cloudinary import uploader

@jwt_required(fresh=True)
def deleteUser(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['idUser'] == id:    
            selectById = User.get(idUser = id)
            if not selectById:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif selectById:
                #picture = "profile"+"_"+currentUser['idUser']
                s = False
                try:
                    public_id = currentUser['picture']
                    print (public_id)
                    cloudinary.uploader.destroy(public_id,invalidate = True)
                    s = True
                except:
                    pass
                if s == True:
                    #User[id].delete()
                    return "a"
                response = {
                    "Message": "Delete Success"
                }
                return responseHandler.ok(response)
            response = {
                "Message": "Delete Invalid"
            }
            return responseHandler.badRequest(response)
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