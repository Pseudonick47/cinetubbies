#!/bin/bash
# Start all services

# Start Backend stack (in detached mode)
docker-compose up -d

# Start Frontend
bash -c 'cd frontend; yarn run dev'
