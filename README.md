# Social media API 

Built with FastAPI and SQLAlchemy 

## Getting Started

### Setup

### ENV Variables
```
#Create .env file
touch .env

#Inside .env, set this variables.
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=
```

### 

```
#Install  packages
pip install -r requirements.txt

#Run a server 
uvicorn app.main:app --reload 

#To view the Swagger documentation.
http://0.0.0.0:8000/docs
