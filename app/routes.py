from app import app
from app.controllers.publisher import listPublisher,createPublisher,readPublisher,updatePublisher,deletePublisher
from app.controllers.user import listUser,createUser,readUser,updateUser,deleteUser
from app.controllers.author import listAuthor,createAuthor,readAuthor,updateAuthor,deleteAuthor
from app.controllers.category import listCategory,createCategory,readCategory,updateCategory,deleteCategory
from app.controllers.book import listBook,createBook,readBook,updateBook,deleteBook
from app.controllers import auth,transaction,token,sendMail


#AUTHOR
app.route('/authors/list',methods = ['GET'])(listAuthor.listAuthors)
app.route('/author/create',methods = ['POST'])(createAuthor.createAuthor)
app.route('/author/read/<id>',methods = ['GET'])(readAuthor.readAuthor)
app.route('/author/update/<id>',methods = ['PATCH'])(updateAuthor.updateAuthor)
app.route('/author/delete/<id>',methods = ['DELETE'])(deleteAuthor.deleteAuthor)


#PUBLISHER
app.route('/publishers/list',methods = ['GET'])(listPublisher.listPublisher)
app.route('/publisher/create',methods = ['POST'])(createPublisher.createPublisher)
app.route('/publisher/read/<id>',methods = ['GET'])(readPublisher.readPublisher)
app.route('/publisher/update/<id>',methods = ['PATCH'])(updatePublisher.updatePublisher)
app.route('/publisher/delete/<id>',methods = ['DELETE'])(deletePublisher.deletePublisher)


#CATEGORY
app.route('/categories/list',methods = ['GET'])(listCategory.listCategory)
app.route('/category/create',methods = ['POST'])(createCategory.createCategory)
app.route('/category/read/<id>',methods = ['GET'])(readCategory.readCategory)
app.route('/category/update/<id>',methods = ['PATCH'])(updateCategory.updateCategory)
app.route('/category/delete/<id>',methods = ['DELETE'])(deleteCategory.deleteCategory)


#BOOK
app.route('/books/list',methods = ['GET'])(listBook.listBooks)
app.route('/book/create',methods = ['POST'])(createBook.createBook)
app.route('/book/read',methods = ['GET'])(createBook.read)
app.route('/book/read/<id>',methods = ['GET'])(readBook.readBook)
app.route('/book/update/<id>',methods = ['PATCH'])(updateBook.updateBook)
app.route('/book/delete/<id>',methods = ['DELETE'])(deleteBook.deleteBook)

#USER
app.route('/users/list',methods = ['GET'])(listUser.listUsers)
app.route('/user/create',methods = ['POST'])(createUser.createUser)
app.route('/user/read/<id>',methods = ['GET'])(readUser.readUser)
app.route('/user/update/<id>',methods = ['PATCH'])(updateUser.updateUser)
app.route('/user/delete/<id>',methods = ['DELETE'])(deleteUser.deleteUser)


#AUTH
app.route('/auth/login',methods = ['POST'])(auth.login)

#TOKEN
app.route('/refresh',methods = ['POST'])(token.refresh)

#SENDMAIL
app.route('/send',methods=['GET'])(sendMail.sendMail)
app.route('/verif',methods = ['GET'])(sendMail.after)

#TRANSACTION
#BORROW
app.route('/list/booked',methods = ['GET'])(transaction.listBooked)
app.route('/list/approved',methods = ['GET'])(transaction.listApproved)
app.route('/list/book',methods = ['GET'])(transaction.listBook)
app.route('/borrow/<idBook>',methods = ['POST'])(transaction.borrowBook)
app.route('/list/accbook',methods = ['GET'])(transaction.listAccBook)
app.route('/accbook/<id>',methods = ['PATCH'])(transaction.accBook)
#RETURN
app.route('/list/return',methods = ['GET'])(transaction.listReturnBook)
app.route('/return/<id>',methods = ['POST'])(transaction.returnBook)
app.route('/list/charge',methods = ['GET'])(transaction.lateCharge)