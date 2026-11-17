from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)        # Ej: "Plan Mensual Ilimitado", "Plan 12 Clases"
    precio = Column(Float, nullable=False)              # Precio en USD
    duracion_dias = Column(Integer, nullable=False)     # Ej: 30, 90, 365
    descripcion = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

class MembershipPayment(Base):
    __tablename__ = "membership_payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    monto_pagado = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)    # Ej: "Pago Móvil", "Zelle", "Efectivo", "Transferencia"
    referencia = Column(String(100), nullable=True)     # Número de referencia bancaria
    estado = Column(String(30), default="activo")       # "activo", "vencido", "pendiente"
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones para acceder fácilmente a los datos
    usuario = relationship("User")
    plan = relationship("Plan")