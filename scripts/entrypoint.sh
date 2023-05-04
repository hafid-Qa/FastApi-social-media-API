#!/bin/bash

# forcedly upgrade database to updated version
python3 -m alembic upgrade head

echo "fast api social is invoked!"
# start grpc server as daemon
export PYTHONPATH=/src

# start  app
python3 -m app.main
