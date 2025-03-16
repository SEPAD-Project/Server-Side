import os
import json

# Function to create a school directory
def create_school(school_name):
    try:
        os.mkdir(school_name)
        print(f"School '{school_name}' created successfully.")
    except FileExistsError:
        print(f"School '{school_name}' already exists.")




