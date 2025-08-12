from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import predict
from app import admin as admin_api
from app.database import run_migration


# ✅ Initialisation de l'application
app = FastAPI(
    title="AI Project Management Predictor",
    description="API to predict project delays and budget overruns using ML",
    version="1.0.0"
)

# ✅ CORS : permet au front React (localhost:3000/5000) d'accéder à l'API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    # "https://mon-site-production.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Inclusion des routers
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(admin_api.router, prefix="/api", tags=["Admin"])

# ✅ Événement au démarrage du serveur
@app.on_event("startup")
def startup_event():
    print("🚀 Running DB migration...")
    run_migration()
    print("✅ Migration terminée.")

# ✅ Route de test
@app.get("/")
def read_root():
    return {"message": "AI Project Management API is running 🚀"}