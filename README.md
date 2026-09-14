# Summative Lab: Full Auth Flask Backend- Productivity App

A mini journal app api with a full IAM flow and Data Integrity.
Built entirely with Flask, Flask-SQLAlchemy, and Marshmallow.

This application implements a **Full IAM Flow** from login, check_sessions, logout, sessions & authorification. 

## Features
### 1.Authentication
This app allows users to signup, login, logout and check_session.

### 2. Authorification
This app restricts users from accessing other users journals by:
    - Every restricted resources is accessed with the users username in the url.
    i.e getting all journals: `/<username>/journals` -> `/mary/journals`
    - For every request made to restricted routes, the user session is checked to prevent other users from accessing your journals.

### 3. Password protection
Every user when signing up must signining with a password.
Every user is authenticated by their password.
Password are stored as hashes in the db.

### 4. Journaling CRUD operations
Users can add new journals, view all, view one, update or delete a journal.


## Technologies Used
### Languages
- Python, Flask

### Package Manager
- Pipenv: Both managing packages and virtual env

### External dependacies
- mashmallow: serialization
- flask-migrate: DB migration
- flask-sqlalchemy: ORM
- flask-restful: modular resource routes
- flask-bcrypt: to hash passwords

### Workflow 
- Git: code workflow managing tool
- Github: store remote repo


## Getting started
To run this program you will need to fork this repo, and install on your local machine.

### Installation & Setup Instructions

Follow these exact steps from the **root directory** of the repository to initialize your environment, create the database tables, and seed records.

1. Active, Install Dependencies & upgrade db
This project uses a local virtual environment configuration. Activate it and install dependencies:

```bash
pipenv install
pipenv shell

cd server
flask db upgrade

```

3. Seed the Database
Execute the population utility script from your root directory to clear past tables and inject a group of fresh records cleanly into your active database file:
```bash
python seed.py
```


### Run Instructions

Start the local development server by executing your main execution file:
```bash
python server/app.py
```
The server will bind to port **`5555`**. You can verify that your configuration is running smoothly by visiting `http://localhost:5555/` in your browser or tool of choice (Postman, cURL, etc.).



## API Endpoints

### Authentification

1. `POST` `/signup` .
Signup.
    Fields required:
        - `username`(must be unique)
        - `password`

2. `POST` `/login`
log in. Fields required: `username`(must be unique), `password`.

3. `GET` `/check_session` 
Check if you are logged in. Returns the user info if logged in.

4. `DELETE` `/<username>/logout` 
Log out


### Journal Full CRUD Operations

1. `GET` `/<username>/journals`
Lists all your journals.

2. `POST` `/<username>/journals`
Add a new journal:
    Required fields:
        - `title`
        - `content`

3. `GET` `/<username>/journals/<int:journal_id>`
View a single journal.

4. `PATCH` `/<username>/journals/<int:journal_id>`
Update a single journal.

5. `DELETE` `/<username>/journals/<int:journal_id>`
View a single journal.


## Project Structure

```text
sqlalchemy-workout-app/
├── server/
│   └── migrations/
│   └── instance/
│   │   └── app.db
│   └── app.py
│   └── models.py
│   └── config.py
│   └── seed.py
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
└── README.md

```

## License
This project is licensed under the MIT License.