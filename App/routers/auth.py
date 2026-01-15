

"""login into your account """


from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import  schemas, models, utils, oauth2
from .. database import get_db

router = APIRouter(
    prefix='/login',

    tags=['Authentication']

    )

#Note OAuth2PasswordRequestForm has by default username and password, can't be called nothing else
# { username: johndoe # this for me, is the user_id 
#   password:xxxxxxxxxxxx
# }



@router.post('/')
# def userlogin(credential: schemas.UserLogin, db: Session = Depends(get_db)):
def userlogin(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_creed = db.query(models.User).filter(models.User.email == user_credential.username.capitalize())
    # print("this db credentials", db_creed)
    
    #first check if email exist 
    db_credential= db_creed.first()
    # print("type of creditinal", type(db_credential))
    # print("this Id credentials", db_credential.id)

    if  db_credential is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email '{user_credential.username}' not found"
        )

    #second check if password exist
    if not utils.verify_password(user_credential.password, db_credential.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid login credentials"
        )
    # once logged in a token will be created which is returned to the user, this will be used to verify other request
    # that will done on the database 
    # Return token
    token=oauth2.create_access_token({"user_id":db_credential.id })
   
  

    return {"access_token":token}






# Note: 
# we verying email and password if that checks out we than create the token
# however to create the token, I used the id, is important to note that this was 
# my decesion and can easily have  used the email to create it. for example:
# token=oauth2.create_access_token({"user_email":user_credential.db_credential.email })





























# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         models.User.email == user_credentials.username).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     # create a token
#     # return token

#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     return {"access_token": access_token, "token_type": "bearer"}


