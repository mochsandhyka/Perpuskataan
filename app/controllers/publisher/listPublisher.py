from app import responseHandler
from app.models.publisher import Publisher
from pony.orm import select

def listPublisher():
    try:
        listPublisher = select(a for a in Publisher)[:]
        data = []
        for i in range(len(listPublisher)):
            data.append(listPublisher[i].to_dict())
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)