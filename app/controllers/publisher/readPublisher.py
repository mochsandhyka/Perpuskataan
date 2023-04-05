from app import responseHandler
from app.models.publisher import Publisher
from pony.orm import select
 
def readPublisher(id):                     
    try:
        readById = Publisher.get(idBookPublisher = id)
        data = readById.to_dict()
        response = {
            "Data": data
        } 
        return responseHandler.ok(response)
    except Exception as err:
            response = {
                "Message": "Publisher Not Found"
            }
            return responseHandler.badRequest(response)