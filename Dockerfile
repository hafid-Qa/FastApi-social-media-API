FROM python:3.9.16-slim-buster

# set the working directory
WORKDIR /app

# install dependencies
COPY ./src/requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY ./src /app

# copy scripts folder
COPY ./scripts /scripts/
RUN chmod -R +x /scripts
ENV PATH="/scripts:${PATH}"
# Set the command to start the FastAPI application
CMD ["entrypoint.sh"]
