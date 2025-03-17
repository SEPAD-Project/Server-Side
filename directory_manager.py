import os
import json
import shutil
from log_handler import log_message

# Define the base path where all schools will be created
BASE_PATH = r"C:\sap-project\schools"

def out(x):
    """Prints the message and logs it using log_handler module."""
    print(x)
    log_message(x)

# Ensure the base path exists
if not os.path.exists(BASE_PATH):
    try:
        os.makedirs(BASE_PATH)
        out('base path created >> C://sap-project//schools')
    except PermissionError:
        out('Permission denied while creating base path >> C://sap-project//schools')

# ---------- School Management Functions ---------- #
def create_school(school_code):
    """
    Creates a new school directory.
    
    Parameters:
        school_code (str): Unique identifier for the school (e.g., '500125')
    """
    school_path = os.path.join(BASE_PATH, school_code)
    try:
        os.mkdir(school_path)
        out(f"School '{school_code}' created successfully at '{school_path}'.")
    except FileExistsError:
        out(f"School '{school_code}' already exists at '{school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create school '{school_code}' at '{school_path}'.")


def edit_school(old_school_code, new_school_code):
    """
    Renames an existing school directory.
    
    Parameters:
        old_school_code (str): Current school name (e.g., '500125')
        new_school_code (str): New school name (e.g., '500126')
    """
    old_school_path = os.path.join(BASE_PATH, old_school_code)
    new_school_path = os.path.join(BASE_PATH, new_school_code)
    try:
        os.rename(old_school_path, new_school_path)
        out(f"School renamed from '{old_school_code}' to '{new_school_code}' successfully.")
    except FileNotFoundError:
        out(f"School '{old_school_code}' does not exist at '{old_school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename school '{old_school_code}' to '{new_school_code}'.")


def delete_school(school_code):
    """
    Permanently deletes a school directory and all its contents.
    
    Parameters:
        school_code (str): Name of the school to delete (e.g., '500125')
    """
    school_path = os.path.join(BASE_PATH, school_code)
    try:
        shutil.rmtree(school_path)  
        out(f"School '{school_code}' and its contents deleted successfully from '{school_path}'.")
    except FileNotFoundError:
        out(f"School '{school_code}' does not exist at '{school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete school '{school_code}' at '{school_path}'.")


# ---------- Class Management Functions ---------- #
def create_class(school_code, class_name):
    """
    Creates a new class directory inside a school.
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        class_name (str): Name of the class to create (e.g., '1051')
    """
    class_path = os.path.join(BASE_PATH, school_code, class_name)
    try:
        os.mkdir(class_path)
        out(f"Class '{class_name}' created in school '{school_code}' successfully at '{class_path}'.")
    except FileExistsError:
        out(f"Class '{class_name}' already exists in school '{school_code}' at '{class_path}'.")
    except FileNotFoundError:
        out(f"School '{school_code}' does not exist at '{os.path.join(BASE_PATH, school_code)}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create class '{class_name}' in school '{school_code}' at '{class_path}'.")


def edit_class(school_code, old_class_name, new_class_name):
    """
    Renames an existing class directory.
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        old_class_name (str): Current class name (e.g., '1051')
        new_class_name (str): New class name (e.g., '1052')
    """
    old_class_path = os.path.join(BASE_PATH, school_code, old_class_name)
    new_class_path = os.path.join(BASE_PATH, school_code, new_class_name)
    try:
        os.rename(old_class_path, new_class_path)
        out(f"Class renamed from '{old_class_name}' to '{new_class_name}' in school '{school_code}' successfully.")
    except FileNotFoundError:
        out(f"Class '{old_class_name}' does not exist in school '{school_code}' at '{old_class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename class '{old_class_name}' to '{new_class_name}' in school '{school_code}'.")


def delete_class(school_code, class_name):
    """
    Permanently deletes a class directory and all its contents.
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        class_name (str): Name of the class to delete (e.g., '1051')
    """
    class_path = os.path.join(BASE_PATH, school_code, class_name)
    try:
        shutil.rmtree(class_path)  
        out(f"Class '{class_name}' deleted from school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Class '{class_name}' does not exist in school '{school_code}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete class '{class_name}' in school '{school_code}' at '{class_path}'.")


# ---------- Student Management Functions ---------- #
def create_student(school_code, class_name, student_code):
    """
    Creates student record with JSON and TXT files.
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        class_name (str): Parent class name (e.g., '1052')
        student_code (str): Unique student identifier (e.g., '09295')
    """
    class_path = os.path.join(BASE_PATH, school_code, class_name)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        with open(student_json_path, 'w') as json_file:
            json.dump({"name": student_code}, json_file)
        with open(student_txt_path, 'w') as txt_file:
            txt_file.write(f"Student Name: {student_code}\n")
        out(f"Student '{student_code}' created in class '{class_name}' of school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Class '{class_name}' does not exist in school '{school_code}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create student '{student_code}' in class '{class_name}' of school '{school_code}' at '{class_path}'.")


def edit_student(school_code, class_name, old_student_code, new_student_code):
    """
    Renames student files .
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        class_name (str): Parent class name (e.g., '1051')
        old_student_code (str): Current student identifier (e.g., '09295')
        new_student_code (str): New student identifier (e.g., '09296')
    """
    class_path = os.path.join(BASE_PATH, school_code, class_name)
    old_student_json_path = os.path.join(class_path, f"{old_student_code}.json")
    old_student_txt_path = os.path.join(class_path, f"{old_student_code}.txt")
    new_student_json_path = os.path.join(class_path, f"{new_student_code}.json")
    new_student_txt_path = os.path.join(class_path, f"{new_student_code}.txt")
    
    try:
        os.rename(old_student_json_path, new_student_json_path)
        os.rename(old_student_txt_path, new_student_txt_path)
        out(f"Student renamed from '{old_student_code}' to '{new_student_code}' in class '{class_name}' of school '{school_code}' successfully.")
    except FileNotFoundError:
        out(f"Student '{old_student_code}' does not exist in class '{class_name}' of school '{school_code}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename student '{old_student_code}' to '{new_student_code}' in class '{class_name}' of school '{school_code}'.")


def delete_student(school_code, class_name, student_code):
    """
    Deletes student records (JSON and TXT files).
    
    Parameters:
        school_code (str): Parent school name (e.g., '500125')
        class_name (str): Parent class name (e.g., '1051')
        student_code (str): Student identifier to delete (e.g., '09295')
    """
    class_path = os.path.join(BASE_PATH, school_code, class_name)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        os.remove(student_json_path)
        os.remove(student_txt_path)
        out(f"Student '{student_code}' deleted from class '{class_name}' of school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Student '{student_code}' does not exist in class '{class_name}' of school '{school_code}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete student '{student_code}' in class '{class_name}' of school '{school_code}' at '{class_path}'.")


# Example usage
if __name__ == "__main__":
    # Sample workflow
    create_school("MySchool")
    create_class("MySchool", "ClassA")
    create_student("MySchool", "ClassA", "JohnDoe")
    edit_student("MySchool", "ClassA", "JohnDoe", "JaneDoe")
    delete_student("MySchool", "ClassA", "JaneDoe")
    delete_class("MySchool", "ClassA")
    delete_school("MySchool")