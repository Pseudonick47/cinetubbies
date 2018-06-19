#!/bin/bash
# Start all services

# Start Backend stack (in detached mode)
docker-compose up -d

if [ "$1" != "production" ];
then
  # Start Frontend dev server
  cd frontend
  yarn run dev
fi