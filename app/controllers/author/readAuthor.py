from app import responseHandler
from app.models.author import BookAuthor
from pony.orm import select
 
def readAuthor(id):                     
    try:
        readById = BookAuthor.get(idBookAuthor = id)
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