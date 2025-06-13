# FastAPI Todo API

A simple Todo List API built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

*   User registration and login (JWT-based authentication).
*   Create, Read, Update, and Delete (CRUD) operations for Todo items.
*   List all todos for a user.
*   List only completed todos for a user.
*   Password hashing using bcrypt.

## Project Structure

```
app/
├── auth/               # Authentication logic (JWT)
│   └── auth.py
├── cruds/              # CRUD operations for database models
│   ├── __init__.py
│   ├── todos_crud.py
│   └── user_crud.py
├── routers/            # API endpoint definitions
│   ├── __init__.py
│   ├── todos.py
│   └── users.py
├── schemas/            # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── todo_schemas.py
│   └── user_schemas.py
├── database.py         # Database setup and session management
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy database models
Pipfile                 # Project dependencies for pipenv
Pipfile.lock
readme.md
todolist.db             # SQLite database file (created automatically)
```

## Setup and Running the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies using Pipenv:**
    Make sure you have `pipenv` installed (`pip install pipenv`).
    ```bash
    pipenv install
    ```

3.  **Activate the virtual environment:**
    ```bash
    pipenv shell
    ```

4.  **Run the application:**
    The application uses Uvicorn to run.
    ```bash
    python app/main.py
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

The API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs` when the application is running.

### User Endpoints (`/users`)

*   `POST /users/create`: Create a new user.
*   `GET /users/{user_id}`: Get user details by ID.
*   `PUT /users/{user_id}`: Update user details.
*   `DELETE /users/{user_id}`: Delete a user.
*   `POST /users/login`: Login a user (expects `application/x-www-form-urlencoded` with `username` (email) and `password`). Returns a JWT token.
*   `POST /users/login/form`: Login a user (expects form data with `email` and `password`). Returns a JWT token.

### Todo Endpoints (`/todos`)

*All Todo endpoints require authentication (Bearer Token).*

*   `POST /todos/newtodos`: Create a new todo.
*   `GET /todos/`: Get all todos for the current user (supports pagination with `skip` and `limit` query parameters).
*   `GET /todos/{todo_id}`: Get a specific todo by ID.
*   `PUT /todos/{todo_id}`: Update an existing todo.
*   `DELETE /todos/{todo_id}`: Delete a todo.
*   `GET /todos/completed/all`: Get all completed todos for the current user.

## Dependencies

*   FastAPI
*   SQLAlchemy
*   Passlib (with bcrypt)
*   python-jose (for JWT)
*   python-multipart
*   Uvicorn (for serving)

```
