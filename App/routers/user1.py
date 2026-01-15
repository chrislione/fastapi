
"""create a new user account"""

from ..import utils, schemas, models
from fastapi import FastAPI, Query, Path, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import oauth2
# from ..oauth2 import get_current_user



router=APIRouter(
    prefix="/users",
 
    tags=["USERS"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(new_user:schemas.UserCreate, db:Session = Depends(get_db)):

    hashed=utils.hashpassword(new_user.password)
    new_user.password=hashed
    new_user.email=new_user.email.capitalize()

    new_user_created = models.User(
        **new_user.model_dump()
    ) 
    db.add(new_user_created)
    db.commit()
    db.refresh(new_user_created)

    return new_user_created


# @router.get("/{id}", response_model=schemas.UserOut)
# def get_payload(id: int, db: Session = Depends(get_db)):
#     payload = db.query(models.User).filter(models.User.id == id).first()

#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} was not found"
#         )

#     return payload

@router.get("/{id}",response_model=schemas.UserOut)
def get_payload(id: int, 
                db: Session = Depends(get_db), 
                get_user_id:int=Depends(oauth2.get_current_user)
                ):
    payload = db.query(models.User).filter(models.User.id == id).first()

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )
    print("this is my id",get_user_id)
    return payload





























