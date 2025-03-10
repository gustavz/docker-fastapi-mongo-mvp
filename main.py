from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as api_router

app = FastAPI()

# Set up CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router)