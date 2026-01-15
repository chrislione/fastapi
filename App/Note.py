# from random import randrange
# from typing import Optional
# from fastapi import FastAPI, Query, Path, HTTPException, Depends, status
# from fastapi import Body, Depends
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor # this will let you get the column in your database 
# # from * import models
# from sqlalchemy.orm import Session
# import  models
# from database import engine, SessionLocal
# models.Base.metadata.create_all(bind=engine)





# app= FastAPI()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/sqlalchemy")
# def test (db: Session = Depends(get_db)):
#     return{"status":"success"}

# # --------------------Database connection---------------------
# try:
#     conn= psycopg2.connect(
#         host='localhost',
#         database= 'fastapi',
#         port='5433',
#         user='postgres',
#         password='Postgres234',
#         cursor_factory= RealDictCursor
#     )
#     cusor=conn.cursor()
#     print("postgrad was successful connected ✅")
# except Exception as error:
#     print("connection failed error:",error)

# class Postm(BaseModel): 
#     #this class makes sure that the data we are sending is in the correct format
#     #The below fields has to match the data we are sending in the body of the request
#     # if the data we are sending does not match the fields in the class, it will raise an error
#     #it carry the infomation form postman or user
#     title: str
#     content: str
#     published:bool=True #this means that published is a required field and it will be set to True by default
#     #you can also set it to yes or no,1 or 0, true or false.
#     # and it will be converted to a boolean value
#     # rating: Optional[int]=None #this means that rating is not a required field and also is keeping 
#     #the data type as integer and it will be set to None by default if not provided
# #--------------------Get all column in the database ---------------------
# cusor.execute("""select * from inventory""")
# db_post=cusor.fetchall()


# #-----------------------------------Posting into the database-----------------------------------   
# #%s is done to avoid data breach, sql injection
# @app.post("/createpost")
# def create_post(post: Postm):
#     cusor.execute(
#                     """INSERT INTO inventory(title, content, published) 
#                     VALUES(%s,%s,%s)RETURNING *""",
#                     (
#                         post.title,
#                         post.content, 
#                         post.published
#                     )
#     )      
#     conn.commit()
#     new_post=cusor.fetchone()
#     return{"data":new_post}


# @app.get("/posts/{id}")
# def get_id(id:int):
#     cusor.execute(
#             """SELECT * FROM inventory
#                 WHERE id= %s  """,

#                 (id,)
#             )
#     post=cusor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   
#     return{"data":post}
# #------------delete--------------------------------
# @app.delete("/deletepost/{id}")
# def del_post(id:int):
#         cusor.execute("""DELETE  
#                         FROM inventory
#                         WHERE id = %s RETURNING *""",
#                         (str(id)) #this also works (id,)
                  
#                   )
#         post=cusor.fetchone()
#         conn.commit()
#         if not post:
#              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#         return {"deleted":post}


# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from fastapi.params import Body
# from fastapi import FastAPI, Query, Path, HTTPException, Depends, status
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# import time
# from sqlalchemy.orm import Session
# from .import models
# from .database import engine, get_db
# from .import schemas
# from passlib.context import CryptContext
# from .import utils
# # from .database import cusor

# # pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
# # class Postm(BaseModel):
# #     title: str
# #     content: str
# #     published: bool = True
 
# models.Base.metadata.create_all(bind=engine)

# app= FastAPI()

# #-----------Get all post without sqlalchemy-------------
# # @app.get("/sqlalchemy")
# # def get_all():
# #     cusor.execute("""select * from inventory""")
# #     db_post=cusor.fetchall()
# #     return{"data":db_post}

# #-----------Get all post sqlalchemy-------------

# @app.get("/sqlalchemy")
# def test (db: Session = Depends(get_db)): # session gives you the ablity to talk to the database like query, get_db is for login
#     get_post= db.query(models.Post).all()
#     return{"data":get_post}

# #---------------------------------------------------------------------------------------------------------------
# #-----------create a post without using sqlalchemy-------------
# # @app.post("/createpost")
# # def create_post(post: Postm):
# #     cusor.execute(
# #                     """INSERT INTO inventory(title, content, published) 
# #                     VALUES(%s,%s,%s)RETURNING *""",
# #                     (
# #                         post.title,
# #                         post.content, 
# #                         post.published
# #                     )
# #     )      
# #     conn.commit()
# #     new_post=cusor.fetchone()
# #     return{"data":new_post}

# # ----------- create a post using  sqlalchemy-------------

# @app.post("/posts")
# def creat_post(post:schemas.Postm, db: Session = Depends(get_db)):
#     # new_post=models.Post(
#     #             title=post.title,
#     #             content=post.content, 
#     #             published=post.published 
#     #             )

#     # the above will work but is ineffecient because lets say you have 50 columns than you have maunelly do this
#     # so the a better is for column to be able to fill it self without maunel typing
#      new_post=models.Post(
#          **post.model_dump() # this will unpack this dictonary 
#          )
#      db.add(new_post)
#      db.commit()
#      db.refresh(new_post)

#      return {"data":new_post}
# #------------------------------------------------------------------------------------------------
# # ---------------Get post by id using sql-------------
# # @app.get("/posts/{id}")
# # def get_id(id:int):
# #     cusor.execute(
# #             """SELECT * FROM inventory
# #                 WHERE id= %s  """,

# #                 (id,)
# #             )
# #     post=cusor.fetchone()
# #     if not post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   
# #     return{"data":post}
# # ----------Get post by id using sqlachlemy--------
# @app.get("/posts/{id}", response_model=schemas.Postm)
# def get_post_id(id:int, db:Session=Depends(get_db)):
#     post=db.query(models.Post).filter(models.Post.id==id).first()
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#     return post


# #------------------------------------------------------------------------
# # ------------------------------delete post--------------------------------


# # @app.delete("/deletepost/{id}")
# # def del_post(id:int):
# #         cusor.execute("""DELETE  
# #                         FROM inventory
# #                         WHERE id = %s RETURNING *""",
# #                         (str(id)) #this also works (id,)
                  
# #                   )
# #         post=cusor.fetchone()
# #         conn.commit()
# #         if not post:
# #              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
# #         return {"deleted":post}

# @app.delete("/deletepost/{id}")
# def del_post(id:int,db:Session=Depends(get_db)):
#     delete_post=db.query(models.Post).filter(models.Post.id==id).delete(synchronize_session=False)
#     # print("delete_post:",delete_post)
#     if not delete_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#     # return{"data":delete_post}
#     db.commit()
#     # delete_=delete_post.delete(synchronize_session=False) 
#     return {"message": f"Post with id {id} deleted"}


# # ----------------------method 2--------------------------------------


# # @app.delete("/seconddeletepost/{id}")
# # def del_post(id:int,db:Session=Depends(get_db)):
# #     delete_post=db.query(models.Post).filter(models.Post.id==id).first()
  
# #     if not delete_post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
# #     db.delete(delete_post)
 
# #     db.commit()
# #     return {"message": f"Post with id {id} deleted"}


# # ----------------------Update --------------------------------------


 

# @app.put("/posts/{id}")
# def update_post(updated_post: schemas.Postm, id: int, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     existing_post = post_query.first()

#     if existing_post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} was not found"
#         )

#     post_query.update(updated_post.model_dump(), synchronize_session=False)
#     db.commit()

#     return {f"Post with id {id} was Updated"
#             : post_query.first()}


 

# # using passlib validate password and email using emailStr
# # @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# # def create_user(user_verify:schemas.UserCreate, db:Session = Depends(get_db)):

# #     hashed_pwd= pwd_context.hash(user_verify.password)
# #     user_verify.password=hashed_pwd

# #     user_ = models.User(
# #         **user_verify.model_dump()
# #     ) 
# #     db.add(user_)
# #     db.commit()
# #     db.refresh(user_)

# #     return user_
# #----------------using pwdlib and argon2-------------------
# from pwdlib import PasswordHash
# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user_verify:schemas.UserCreate, db:Session = Depends(get_db)):

#     hashed=utils.hashpassword(user_verify.password)
#     user_verify.password=hashed

#     user_ = models.User(
#         **user_verify.model_dump()
#     ) 
#     db.add(user_)
#     db.commit()
#     db.refresh(user_)

#     return user_


# @app.get("/users/{id}", response_model= schemas.UserOut)
# def get_payload(id:int,  db:Session = Depends(get_db)):
#     payload_query=db.query(models.User).filter(models.User.id==id)
    
#     if payload_query ==None:
#          raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} was not found"
#         )
#     payload=payload_query.first()
#     return payload

































































# # # from fastapi import FastAPI
# # # from fastapi.middleware.cors import CORSMiddleware

# # # from . import models
# # # from .database import engine
# # # from .routers import post, user, auth, vote
# # # from .config import settings


# # # # models.Base.metadata.create_all(bind=engine)

# # # app = FastAPI()

# # # origins = ["*"]

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=origins,
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # app.include_router(post.router)
# # # app.include_router(user.router)
# # # app.include_router(auth.router)
# # # app.include_router(vote.router)



