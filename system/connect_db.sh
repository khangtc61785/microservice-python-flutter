#!/bin/bash

CONTAINER_NAME="my-postgres"

echo "Connect postgresql"
docker exec -it $CONTAINER_NAME psql -U postgres