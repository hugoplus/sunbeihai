#!/bin/bash

until cd /code/sunbeihai
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A sunbeihai worker -l info