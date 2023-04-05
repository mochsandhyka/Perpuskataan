from app import responseHandler
from app.models.bookCategory import BookCategory
from pony.orm import select


def listCategory():
    try:
        listCategory = select(a for a in BookCategory)[:]
        data = []
        for i in range(len(listCategory)):
            data.append(listCategory[i].to_dict())
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)