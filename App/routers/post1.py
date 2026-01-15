from ..import utils, schemas, models
from fastapi import FastAPI, Query, Path, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..import oauth2
from typing import Optional

router=APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)
@router.post("/", response_model=schemas.Post)
def creat_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    # new_post=models.Post(
    #             title=post.title,
    #             content=post.content, 
    #             published=post.published 
    #             )
     print("current_user", current_user)
    # the above will work but is ineffecient because lets say you have 50 columns than you have maunelly do this
    # so the a better is for column to be able to fill it self without maunel typing
     new_post=models.Post( owner_id=current_user.id,
         **post.model_dump() # this will unpack this dictonary 
         )
     db.add(new_post)
     db.commit()
     db.refresh(new_post)

     return new_post

@router.get("/{id}", response_model=schemas.Postm)
def get_post_id(id:int, db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return post

# @router.get("/")
# def get_all_post(db:Session=Depends(get_db),limits:int=3, search:Optional[str]=('')):
    
#     all_post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limits).all()

#     if not all_post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND)
#     return all_post


@router.get("/")
def get_all_post(db: Session = Depends(get_db), limit: int = 3, search: str = ""):
    if not get_all_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return (
        db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).all()
    )
