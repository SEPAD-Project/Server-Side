import os
import json
import shutil
import time 
import platform

def get_base_paths():
    """Return appropriate paths based on the operating system"""
    system = platform.system().lower()
    
    if system == 'windows':
        return {
            'log_file': r"C:\sap-project\log.txt",
            'schools_dir': r"C:\sap-project\server\schools"
        }
    else:  # Linux, macOS, etc.
        home_dir = os.path.expanduser("~")
        return {
            'log_file': os.path.join(home_dir, "sap-project", "log.txt"),
            'schools_dir': os.path.join(home_dir, "sap-project", "server", "schools")
        }

PATHS = get_base_paths()

def log_message(message):
    LOG_PATH = PATHS['log_file']
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, 'a') as file:
        file.write(f"[{formatted_time}] {message}\n")

# Define the base path where all schools will be created
BASE_PATH = PATHS['schools_dir']
print(BASE_PATH)

def out(x):
    """Prints the message and logs it using log_handler module."""
    print(x)
    log_message(x)

# Ensure the base path exists
if not os.path.exists(BASE_PATH):
    try:
        os.makedirs(BASE_PATH)
        out(f'base path created >> {BASE_PATH}')
    except PermissionError:
        out(f'Permission denied while creating base path >> {BASE_PATH}')

# ---------- School Management Functions ---------- #
def dm_create_school(school_id):
    """
    Creates a new school directory.
    
    Parameters:
        school_id (str): Unique identifier for the school (e.g., '500125')
    """
    school_path = os.path.join(BASE_PATH, school_id)
    try:
        os.mkdir(school_path)
        out(f"School '{school_id}' created successfully at '{school_path}'.")
    except FileExistsError:
        out(f"School '{school_id}' already exists at '{school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create school '{school_id}' at '{school_path}'.")


def dm_edit_school(old_school_id, new_school_id):
    """
    Renames an existing school directory.
    
    Parameters:
        old_school_id (str): Current school name (e.g., '500125')
        new_school_id (str): New school name (e.g., '500126')
    """
    old_school_path = os.path.join(BASE_PATH, old_school_id)
    new_school_path = os.path.join(BASE_PATH, new_school_id)
    try:
        os.rename(old_school_path, new_school_path)
        out(f"School renamed from '{old_school_id}' to '{new_school_id}' successfully.")
    except FileNotFoundError:
        out(f"School '{old_school_id}' does not exist at '{old_school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename school '{old_school_id}' to '{new_school_id}'.")


def dm_delete_school(school_id):
    """
    Permanently deletes a school directory and all its contents.
    
    Parameters:
        school_id (str): Name of the school to delete (e.g., '500125')
    """
    school_path = os.path.join(BASE_PATH, school_id)
    try:
        shutil.rmtree(school_path)  
        out(f"School '{school_id}' and its contents deleted successfully from '{school_path}'.")
    except FileNotFoundError:
        out(f"School '{school_id}' does not exist at '{school_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete school '{school_id}' at '{school_path}'.")


# ---------- Class Management Functions ---------- #
def dm_create_class(school_id, class_id):
    """
    Creates a new class directory inside a school.
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        class_id (str): Name of the class to create (e.g., '1051')
    """
    class_path = os.path.join(BASE_PATH, school_id, class_id)
    try:
        os.mkdir(class_path)
        out(f"Class '{class_id}' created in school '{school_id}' successfully at '{class_path}'.")
    except FileExistsError:
        out(f"Class '{class_id}' already exists in school '{school_id}' at '{class_path}'.")
    except FileNotFoundError:
        out(f"School '{school_id}' does not exist at '{os.path.join(BASE_PATH, school_id)}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create class '{class_id}' in school '{school_id}' at '{class_path}'.")


def dm_edit_class(school_id, old_class_id, new_class_id):
    """
    Renames an existing class directory.
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        old_class_id (str): Current class name (e.g., '1051')
        new_class_id (str): New class name (e.g., '1052')
    """
    old_class_path = os.path.join(BASE_PATH, school_id, old_class_id)
    new_class_path = os.path.join(BASE_PATH, school_id, new_class_id)
    try:
        os.rename(old_class_path, new_class_path)
        out(f"Class renamed from '{old_class_id}' to '{new_class_id}' in school '{school_id}' successfully.")
    except FileNotFoundError:
        out(f"Class '{old_class_id}' does not exist in school '{school_id}' at '{old_class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename class '{old_class_id}' to '{new_class_id}' in school '{school_id}'.")


def dm_delete_class(school_id, class_id):
    """
    Permanently deletes a class directory and all its contents.
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        class_id (str): Name of the class to delete (e.g., '1051')
    """
    class_path = os.path.join(BASE_PATH, school_id, class_id)
    try:
        shutil.rmtree(class_path)  
        out(f"Class '{class_id}' deleted from school '{school_id}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Class '{class_id}' does not exist in school '{school_id}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete class '{class_id}' in school '{school_id}' at '{class_path}'.")


# ---------- Student Management Functions ---------- #
def dm_create_student(school_id, class_id, student_code):
    """
    Creates student record with JSON and TXT files.
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        class_id (str): Parent class name (e.g., '1052')
        student_code (str): Unique student identifier (e.g., '09295')
    """
    class_path = os.path.join(BASE_PATH, school_id, class_id)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        with open(student_json_path, 'w') as json_file:
            json.dump({"name": student_code}, json_file)
        with open(student_txt_path, 'w') as txt_file:
            txt_file.write(f"Student Name: {student_code}\n")
        out(f"Student '{student_code}' created in class '{class_id}' of school '{school_id}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Class '{class_id}' does not exist in school '{school_id}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to create student '{student_code}' in class '{class_id}' of school '{school_id}' at '{class_path}'.")


def dm_edit_student(school_id, class_id, old_student_code, new_student_code):
    """
    Renames student files .
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        class_id (str): Parent class name (e.g., '1051')
        old_student_code (str): Current student identifier (e.g., '09295')
        new_student_code (str): New student identifier (e.g., '09296')
    """
    class_path = os.path.join(BASE_PATH, school_id, class_id)
    old_student_json_path = os.path.join(class_path, f"{old_student_code}.json")
    old_student_txt_path = os.path.join(class_path, f"{old_student_code}.txt")
    new_student_json_path = os.path.join(class_path, f"{new_student_code}.json")
    new_student_txt_path = os.path.join(class_path, f"{new_student_code}.txt")
    
    try:
        os.rename(old_student_json_path, new_student_json_path)
        os.rename(old_student_txt_path, new_student_txt_path)
        out(f"Student renamed from '{old_student_code}' to '{new_student_code}' in class '{class_id}' of school '{school_id}' successfully.")
    except FileNotFoundError:
        out(f"Student '{old_student_code}' does not exist in class '{class_id}' of school '{school_id}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to rename student '{old_student_code}' to '{new_student_code}' in class '{class_id}' of school '{school_id}'.")


def dm_delete_student(school_id, class_id, student_code):
    """
    Deletes student records (JSON and TXT files).
    
    Parameters:
        school_id (str): Parent school name (e.g., '500125')
        class_id (str): Parent class name (e.g., '1051')
        student_code (str): Student identifier to delete (e.g., '09295')
    """
    class_path = os.path.join(BASE_PATH, school_id, class_id)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        os.remove(student_json_path)
        os.remove(student_txt_path)
        out(f"Student '{student_code}' deleted from class '{class_id}' of school '{school_id}' successfully at '{class_path}'.")
    except FileNotFoundError:
        out(f"Student '{student_code}' does not exist in class '{class_id}' of school '{school_id}' at '{class_path}'.")
    except PermissionError:
        out(f"Permission denied: Unable to delete student '{student_code}' in class '{class_id}' of school '{school_id}' at '{class_path}'.")


# Example usage
if __name__ == "__main__":
    # Sample workflow
    dm_create_school("MySchool")
    dm_create_class("MySchool", "ClassA")
    dm_create_student("MySchool", "ClassA", "JohnDoe")
    dm_edit_student("MySchool", "ClassA", "JohnDoe", "JaneDoe")
    dm_delete_student("MySchool", "ClassA", "JaneDoe")
    dm_delete_class("MySchool", "ClassA")
    dm_delete_school("MySchool")