from flask_jwt_extended import jwt_required
from flask_mail import Message
from app import mail

@jwt_required()
def sendMail():
    # mail = mt.MailFromTemplate(
    # sender= mt.Address(email="mailtrap@example.com", name="Mailtrap Test"),
    # to=[mt.Address(email="your@email.com")],
    # template_uuid="2f45b0aa-bbed-432f-95e4-e145e1965ba2",
    # template_variables={"user_name": "John Doe"},
    # )

    #client = mt.MailtrapClient(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5MzgzMTc5LCJqdGkiOiJhNjhiYTllNy1kYjM1LTRmYTEtOTk3ZC1mMDUyOWY5ZTI0M2IiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7ImlkVXNlciI6IjYxNjgwYmIxLTY1M2ItNDg3Ni1hOTMxLTQ2ODk2NTViMjkxNyIsInJvbGUiOiJBZG1pbiJ9LCJuYmYiOjE2NzkzODMxNzksImV4cCI6MTY3OTM4Njc3OX0.RMMZ17MAW9wuQP8dsI6uixod_oD1jsxuXZjBAAl0wuo")
    # client.send(mail)
    currentEmail = "wui"
    msg =   Message('Verification Email', 
            sender =   'Admin@perpus.takaan', 
            recipients = [currentEmail])
    msg.body = f"Click this link to acc http://192.168.1.62:5000/verif"
    mail.send(msg)
    return "Message sent!"

def after():
    return "Success"