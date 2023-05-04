# Social media API 

Built with FastAPI and SQLAlchemy 

## Getting Started

### Setup

### ENV Variables
```
#Create .env file
touch .env

#Inside .env, set this variables.
DATABASE_TYPE=postgresql
DATABASE_DRIVER=psycopg2
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
DATABASE_NAME=changeme
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=changeme
# JWT
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

## Docker
```
 docker-compose up
```

## Test
```
 docker-compose run api pytest --verbose
```

#To view the Swagger documentation.
http://0.0.0.0:8000/docs
