#!/bin/bash

# Exit on error
set -e

# Print commands
set -x

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the database initialization script
python init_db.py 