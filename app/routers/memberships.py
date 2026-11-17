from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app.core.database import get_db
from app.models.membership import Plan, MembershipPayment
from app.models.user import User
from app.schemas.membership import PlanCreate, PlanResponse, PaymentCreate, PaymentResponse
from app.routers.users import get_current_user

router = APIRouter(
    prefix="/memberships",
    tags=["Membresías y Pagos"]
)

# --- Rutas de Planes ---
@router.post("/plans", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    """Crea un nuevo plan de suscripción en el Box."""
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/plans", response_model=List[PlanResponse])
def get_active_plans(db: Session = Depends(get_db)):
    """Lista todos los planes disponibles y activos en el Box."""
    return db.query(Plan).filter(Plan.is_active == True).all()

# --- Rutas de Pagos de Atletas ---
@router.post("/pay", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def register_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra el pago de una membresía para el atleta autenticado."""
    plan = db.query(Plan).filter(Plan.id == payment.plan_id, Plan.is_active == True).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El plan seleccionado no existe o no está disponible."
        )

    inicio = payment.fecha_inicio or date.today()
    fin = inicio + timedelta(days=plan.duracion_dias)

    new_payment = MembershipPayment(
        user_id=current_user.id,
        plan_id=plan.id,
        monto_pagado=plan.precio,
        metodo_pago=payment.metodo_pago,
        referencia=payment.referencia,
        estado="activo",
        fecha_inicio=inicio,
        fecha_fin=fin
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/my-history", response_model=List[PaymentResponse])
def get_my_memberships(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Muestra el historial de membresías y pagos del atleta autenticado."""
    return db.query(MembershipPayment).filter(MembershipPayment.user_id == current_user.id).all()