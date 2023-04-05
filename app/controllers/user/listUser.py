from app import responseHandler
from app.models.user import User
from pony.orm import select

def listUsers():
    try:
        listUser = select(a for a in User)[:]
        data = []
        for i in range(len(listUser)):
            data.append(listUser[i].to_dict())
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)