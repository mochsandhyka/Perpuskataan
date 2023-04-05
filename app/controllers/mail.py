from flask_mail import Message

def sendEmail(email,messageBody,subjectBody):
    sendMail = Message(
                 subject = subjectBody,
                 sender = 'upgradelvel@gmail.com',
                 recipients = [email],
                 body= messageBody
            )
    return sendMail