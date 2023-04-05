import hashlib,os


def hashPassword(password):
    hashpassword = hashlib.md5((password+os.getenv("SALT_PASSWORD")).encode()).hexdigest()
    return hashpassword
