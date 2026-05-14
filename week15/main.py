from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI(
    title="User Management API",
    description="A FastAPI project with file persistence",
    version="1.0.0"
)

app.include_router(users_router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "FastAPI User Management API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is working correctly!"}