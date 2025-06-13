# file: app/main.py

from fastapi import FastAPI
from app.routers import todos, users
import uvicorn
from app.database import Base, engine
from app import models

app = FastAPI(title="Todo API") # create the FastAPI app

app.include_router(todos.router) #include the todos router
app.include_router(users.router) #include the users router

models.Base.metadata.create_all(bind=engine) # create the database tables















if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
