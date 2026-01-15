from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers.config import settings

# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql+psycopg2://{settings.database_username}:"
#     f"{settings.database_password}@{settings.database_hostname}:"
#     f"{settings.database_port}/{settings.database_name}"
# )
# print("✅😊SQLALCHEMY_DATABASE_URL",SQLALCHEMY_DATABASE_URL)

SQLALCHEMY_DATABASE_URL = f"{settings.database_type}+{settings.database_driver}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Postgres234@localhost:5433/fastapi"

#engine is responsible for establishing connecting sqlalchemy to postgre
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# However to talk to the database you'll need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base sets up a starting point so you can easily create and manage 
# tables in your database using Python classes.

# When you use it, you’re basically saying:
# Any class I make from this base should automatically 
# be treated like a table in my database
Base = declarative_base()


def get_db():
    db = SessionLocal()
    print("postgrad was successful connected ✅😊")
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='password123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)




#----------------------using postgre--------------------------
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