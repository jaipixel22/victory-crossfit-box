from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from datetime import datetime, date
from app.core.database import Base

class WOD(Base):
    __tablename__ = "wods"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)        # Ej: "Fran", "Murph", "WOD Fuerza"
    tipo = Column(String(50), nullable=False)           # Ej: "AMRAP", "For Time", "EMOM", "Fuerza"
    descripcion = Column(Text, nullable=False)          # Ejercicios, repeticiones y pesos RX/Scaled
    fecha_programada = Column(Date, default=date.today, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)