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

# Function to delete the school directory
def delete_school(school_name):
    try:
        os.rmdir(school_name)
        print(f"School '{school_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"School '{school_name}' does not exist.")
    except OSError:
        print(f"School '{school_name}' is not empty.")

# Function to create a class directory inside the school directory
def create_class(school_name, class_name):
    class_path = os.path.join(school_name, class_name)
    try:
        os.mkdir(class_path)
        print(f"Class '{class_name}' created in school '{school_name}' successfully.")
    except FileExistsError:
        print(f"Class '{class_name}' already exists in school '{school_name}'.")
    except FileNotFoundError:
        print(f"School '{school_name}' does not exist.")

# Function to edit the name of a class directory
def edit_class(school_name, old_class_name, new_class_name):
    old_class_path = os.path.join(school_name, old_class_name)
    new_class_path = os.path.join(school_name, new_class_name)
    try:
        os.rename(old_class_path, new_class_path)
        print(f"Class renamed from '{old_class_name}' to '{new_class_name}' in school '{school_name}' successfully.")
    except FileNotFoundError:
        print(f"Class '{old_class_name}' does not exist in school '{school_name}'.")

# Function to delete a class directory
def delete_class(school_name, class_name):
    class_path = os.path.join(school_name, class_name)
    try:
        os.rmdir(class_path)
        print(f"Class '{class_name}' deleted from school '{school_name}' successfully.")
    except FileNotFoundError:
        print(f"Class '{class_name}' does not exist in school '{school_name}'.")
    except OSError:
        print(f"Class '{class_name}' is not empty.")

