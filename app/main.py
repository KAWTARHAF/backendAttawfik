from fastapi import FastAPI
from app.api import predict,user

from db_init import run_migration





app = FastAPI(
    title="AI Project Management Predictor",
    description="API to predict project delays and budget overruns using ML",
    version="1.0.0"
)

# Include the prediction router
app.include_router(predict.router, prefix="/api")
app.include_router(user.router, prefix="/api")     
