from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)
