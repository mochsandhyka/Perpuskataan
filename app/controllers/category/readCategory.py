from app import responseHandler
from app.models.bookCategory import BookCategory
from pony.orm import select
 
def readCategory(id):                     
    try:
        readById = BookCategory.get(idBookCategory = id)
        data = readById.to_dict()
        response = {
            "Data": data
        } 
        return responseHandler.ok(response)
    except Exception as err:
            response = {
                "Message": "Author Not Found"
            }
            return responseHandler.badRequest(response)