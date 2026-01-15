# from passlib.context import CryptContext
from pwdlib import PasswordHash


#------------------old--------------
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash(password: str):
#     return pwd_context.hash(password)


# def verify(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)




#currently been used
password_hash = PasswordHash.recommended()

def hashpassword(password: str):
    
    hash_password=password_hash.hash(password)
    return hash_password


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)