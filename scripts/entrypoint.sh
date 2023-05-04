#!/bin/bash

# forcedly upgrade database to updated version
python3 -m alembic upgrade head

# run initializing
# python3 initialize.py

echo "fast api social is invoked!"
# start grpc server as daemon
export PYTHONPATH=/app
# nohup python3 -u grpc_server/run_server.py 50052 # > grpc_server/log 2>&1 &

# start  app
python3 -m app.main
