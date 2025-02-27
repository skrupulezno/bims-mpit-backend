from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth_routes, profile_routes, user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3002",
    "http://138.124.20.90:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, tags=["auth"])
app.include_router(profile_routes.router, tags=["profile"])
app.include_router(user_routes.router, tags=["users"])
