from app import responseHandler
from app.models.author import BookAuthor
from pony.orm import select

def listAuthors():
    try:
        listAuthors = select(a for a in BookAuthor)[:]
        data = []
        for i in range(len(listAuthors)):
            data.append(listAuthors[i].to_dict())
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)