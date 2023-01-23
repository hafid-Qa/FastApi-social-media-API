from sqlite3 import SQLITE_LIMIT_ATTACHED
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
ALCHEMY_DATABASE_URL = "postgresql://@localhost/fast_api_dev"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
