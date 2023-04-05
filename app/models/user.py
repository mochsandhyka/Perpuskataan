from ._base import db,Required,PrimaryKey,Set,date,Optional,uuid


class User(db.Entity):
    _table_ = "tbl_user"
    idUser = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_user')
    username = Required(str,unique = True)
    email = Required(str,unique = True)
    password = Required(str)
    name = Optional(str,nullable = True)
    gender = Optional(str,nullable = True)
    address = Optional(str, nullable = True)
    city = Optional(str, nullable = True)
    phoneNumber = Optional(str,column='phone_number',nullable=True)
    dateRegister = Required(date,column='date_register')
    picture = Optional(str,nullable = True)
    role = Required(str)
    isActivate = Required(bool,column = 'is_activate')
    borrowedbook = Set('BorrowedBook')
    returnbook= Set('ReturnBook')

