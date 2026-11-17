from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.database import engine, Base
from app.models import user, wod, membership
from app.routers import users, wods, memberships

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Victory CrossFit Box API",
    description="Backend para la gestión de atletas, WODs, reservas y membresías.",
    version="1.0.0"
)

# Configuración de CORS para permitir conexiones desde navegadores y teléfonos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se restringe al dominio del Box
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de la API
app.include_router(users.router)
app.include_router(wods.router)
app.include_router(memberships.router)

# Servir la interfaz móvil desde la ruta /app
os.makedirs("frontend", exist_ok=True)
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def read_root():
    return {"mensaje": "API activa. Entra a /app para ver la interfaz móvil."}