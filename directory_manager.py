import os
import json
import shutil

# Define the base path where all schools will be created
BASE_PATH = "C://sap-project//schools"

# Ensure the base path exists
if not os.path.exists(BASE_PATH):
    try:
        os.makedirs(BASE_PATH)
    except PermissionError:
        print(f"Permission denied .")

# Function to create a school directory
def create_school(school_code):
    school_path = os.path.join(BASE_PATH, school_code)
    try:
        os.mkdir(school_path)
        print(f"School '{school_code}' created successfully at '{school_path}'.")
    except FileExistsError:
        print(f"School '{school_code}' already exists at '{school_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to create school '{school_code}' at '{school_path}'.")

# Function to edit the code of the school directory
def edit_school(old_school_code, new_school_code):
    old_school_path = os.path.join(BASE_PATH, old_school_code)
    new_school_path = os.path.join(BASE_PATH, new_school_code)
    try:
        os.rename(old_school_path, new_school_path)
        print(f"School renamed from '{old_school_code}' to '{new_school_code}' successfully.")
    except FileNotFoundError:
        print(f"School '{old_school_code}' does not exist at '{old_school_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to rename school '{old_school_code}' to '{new_school_code}'.")

# Function to delete the school directory
def delete_school(school_code):
    school_path = os.path.join(BASE_PATH, school_code)
    try:
        shutil.rmtree(school_path)  
        print(f"School '{school_code}' and its contents deleted successfully from '{school_path}'.")
    except FileNotFoundError:
        print(f"School '{school_code}' does not exist at '{school_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to delete school '{school_code}' at '{school_path}'.")

# Function to create a class directory inside the school directory
def create_class(school_code, class_code):
    class_path = os.path.join(BASE_PATH, school_code, class_code)
    try:
        os.mkdir(class_path)
        print(f"Class '{class_code}' created in school '{school_code}' successfully at '{class_path}'.")
    except FileExistsError:
        print(f"Class '{class_code}' already exists in school '{school_code}' at '{class_path}'.")
    except FileNotFoundError:
        print(f"School '{school_code}' does not exist at '{os.path.join(BASE_PATH, school_code)}'.")
    except PermissionError:
        print(f"Permission denied: Unable to create class '{class_code}' in school '{school_code}' at '{class_path}'.")

# Function to edit the code of a class directory
def edit_class(school_code, old_class_code, new_class_code):
    old_class_path = os.path.join(BASE_PATH, school_code, old_class_code)
    new_class_path = os.path.join(BASE_PATH, school_code, new_class_code)
    try:
        os.rename(old_class_path, new_class_path)
        print(f"Class renamed from '{old_class_code}' to '{new_class_code}' in school '{school_code}' successfully.")
    except FileNotFoundError:
        print(f"Class '{old_class_code}' does not exist in school '{school_code}' at '{old_class_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to rename class '{old_class_code}' to '{new_class_code}' in school '{school_code}'.")

# Function to delete a class directory
def delete_class(school_code, class_code):
    class_path = os.path.join(BASE_PATH, school_code, class_code)
    try:
        shutil.rmtree(class_path)  
        print(f"Class '{class_code}' deleted from school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        print(f"Class '{class_code}' does not exist in school '{school_code}' at '{class_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to delete class '{class_code}' in school '{school_code}' at '{class_path}'.")

# Function to create a student with JSON and TXT files
def create_student(school_code, class_code, student_code):
    class_path = os.path.join(BASE_PATH, school_code, class_code)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        with open(student_json_path, 'w') as json_file:
            json.dump({"name": student_code}, json_file)
        with open(student_txt_path, 'w') as txt_file:
            txt_file.write(f"Student Name: {student_code}\n")
        print(f"Student '{student_code}' created in class '{class_code}' of school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        print(f"Class '{class_code}' does not exist in school '{school_code}' at '{class_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to create student '{student_code}' in class '{class_code}' of school '{school_code}' at '{class_path}'.")

# Function to edit the name of a student
def edit_student(school_code, class_code, old_student_code, new_student_code):
    class_path = os.path.join(BASE_PATH, school_code, class_code)
    old_student_json_path = os.path.join(class_path, f"{old_student_code}.json")
    old_student_txt_path = os.path.join(class_path, f"{old_student_code}.txt")
    new_student_json_path = os.path.join(class_path, f"{new_student_code}.json")
    new_student_txt_path = os.path.join(class_path, f"{new_student_code}.txt")
    
    try:
        os.rename(old_student_json_path, new_student_json_path)
        os.rename(old_student_txt_path, new_student_txt_path)
        print(f"Student renamed from '{old_student_code}' to '{new_student_code}' in class '{class_code}' of school '{school_code}' successfully.")
    except FileNotFoundError:
        print(f"Student '{old_student_code}' does not exist in class '{class_code}' of school '{school_code}' at '{class_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to rename student '{old_student_code}' to '{new_student_code}' in class '{class_code}' of school '{school_code}'.")

# Function to delete a student
def delete_student(school_code, class_code, student_code):
    class_path = os.path.join(BASE_PATH, school_code, class_code)
    student_json_path = os.path.join(class_path, f"{student_code}.json")
    student_txt_path = os.path.join(class_path, f"{student_code}.txt")
    
    try:
        os.remove(student_json_path)
        os.remove(student_txt_path)
        print(f"Student '{student_code}' deleted from class '{class_code}' of school '{school_code}' successfully at '{class_path}'.")
    except FileNotFoundError:
        print(f"Student '{student_code}' does not exist in class '{class_code}' of school '{school_code}' at '{class_path}'.")
    except PermissionError:
        print(f"Permission denied: Unable to delete student '{student_code}' in class '{class_code}' of school '{school_code}' at '{class_path}'.")

# Example usage
if __name__ == "__main__":
    create_school("MySchool")
    create_class("MySchool", "ClassA")
    create_student("MySchool", "ClassA", "JohnDoe")
    edit_student("MySchool", "ClassA", "JohnDoe", "JaneDoe")
    delete_student("MySchool", "ClassA", "JaneDoe")
    delete_class("MySchool", "ClassA")
    delete_school("MySchool")