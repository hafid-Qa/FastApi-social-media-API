from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# only needed incase file main_with_psycop is the main file
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = "postgresql://@localhost/fast_api_dev"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# only needed incase file main_with_psycop is the main file
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fast_api_dev", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection established...")
#         break
#     except Exception as error:
#         print({"error": error})
#         time.sleep(2)
