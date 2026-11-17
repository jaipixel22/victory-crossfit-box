from pydantic import BaseModel
from datetime import date, datetime

class WODBase(BaseModel):
    titulo: str          # Ej: "Fran", "Murph"
    tipo: str            # Ej: "AMRAP", "For Time", "EMOM"
    descripcion: str     # Ejercicios, repeticiones y pesos
    fecha_programada: date

class WODCreate(WODBase):
    pass

class WODResponse(WODBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True