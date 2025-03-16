import os
import json

# Function to create a school directory
def create_school(school_name):
    try:
        os.mkdir(school_name)
        print(f"School '{school_name}' created successfully.")
    except FileExistsError:
        print(f"School '{school_name}' already exists.")

# Function to edit the name of the school directory
def edit_school(old_school_name, new_school_name):
    try:
        os.rename(old_school_name, new_school_name)
        print(f"School renamed from '{old_school_name}' to '{new_school_name}' successfully.")
    except FileNotFoundError:
        print(f"School '{old_school_name}' does not exist.")



