from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# --- Esquemas para Planes ---
class PlanBase(BaseModel):
    nombre: str
    precio: float
    duracion_dias: int
    descripcion: Optional[str] = None
    is_active: bool = True

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id: int

    class Config:
        from_attributes = True

# --- Esquemas para Pagos y Membresías ---
class PaymentCreate(BaseModel):
    plan_id: int
    metodo_pago: str             # Ej: "Pago Móvil", "Zelle", "Efectivo"
    referencia: Optional[str] = None
    fecha_inicio: Optional[date] = None  # Si no se envía, inicia hoy

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    monto_pagado: float
    metodo_pago: str
    referencia: Optional[str]
    estado: str
    fecha_inicio: date
    fecha_fin: date
    created_at: datetime

    class Config:
        from_attributes = True