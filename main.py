from fastapi import FastAPI
from routers import materials
from database import Base, engine

app = FastAPI()

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app.include_router(materials.router)
