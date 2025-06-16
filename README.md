# Server-Side
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Server-Side/blob/main/README.md)
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Server-Side/blob/main/README.fa.md)


**README in English** 

---

## 📁 Server-Side Repository

This repository contains all server-side code for our project, organized into 4 main directories:

### 1. 📡 `apis`
Flask-based API services currently running on the server. This includes all endpoints and business logic for our backend services.

### 2. 🖥️ `dashboard`
An admin dashboard for server management. Features include:
- API monitoring
- Start/stop/restart functionality
- Server status overview

### 3. 🌐 `website`
**Note:** Contains code used in the web repository as a submodule in the backend of the website.

### 4. 🗃️ `database`
*(Legacy code)* Contains:
- Database schema creation scripts
- Table definitions
- Query execution utilities

**Note:** This is mostly deprecated as the database and tables are now automatically created by the website (in Web repository).

---

# ⚙️ Setting up APIs

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```bash
git clone https://github.com/SEPAD-Project/Server-Side.git
```
Then, navigate to the repository directory:
```bash
cd Server-Side
```

## Installing Dependencies
   1. Create a virtual environment:
      ```bash
      python -m venv .venv
      ```
   2. Activate the virtual environment:
      ```bash
      .venv\Scripts\activate.bat
      ```
    3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running apis using Control Server
   1. Navigate to dashboard directory:
        ```bash
        cd dashboard
        ```
   2. Run control_server.py:
        ```bash
        python control_server.py
        ```
   3. Open Control server page and login by go to http://localhost:800
   4. Run each api by click on start button in apis containers  



