from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
# from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
from App import schemas, models, utils
from .routers.config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute
expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict, expires_delta=expires_delta ):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# this part what you need when you trying to call a resources that needs to authication to access aka login
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM]) # remember once you decode this parameter you'll see what is passed in 
                                                                     # as the data when the token was begin created, in my case I passed in a 
                                                                     # an id ("user_id":user_credential.db_credential.id) from the users table and USer class 
        user_id:int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=user_id)

    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data

# this is what is passed in as a depends on your request to make sure user is 
# login, ie they have there tokens 
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
     








































































































































# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from . import schemas, database, models
# from fastapi import Depends, status, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from .config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# # SECRET_KEY
# # Algorithm
# # Expriation time

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# def create_access_token(data: dict):
#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt


# def verify_access_token(token: str, credentials_exception):

#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id: str = payload.get("user_id")
#         if id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id=id)
#     except JWTError:
#         raise credentials_exception

#     return token_data


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                           detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

#     token = verify_access_token(token, credentials_exception)

#     user = db.query(models.User).filter(models.User.id == token.id).first()

#     return user
