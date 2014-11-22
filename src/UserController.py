import hashlib
import uuid

class UserController:

    @staticmethod
    def salt_password(password, salt=None):
        if salt == None:
            salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        return (hashed_password, salt)