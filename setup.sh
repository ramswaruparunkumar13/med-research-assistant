#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Done
echo "Environment setup complete."
echo " No .env file needed. You’re using a local model."





