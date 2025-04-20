from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.database import SessionLocal
from app.models import Usuario
from app.utils import create_access_token, verify_token
from app.config import settings

router = APIRouter()

# Admin fixo
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/solicitar-acesso")
def solicitar_acesso(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter_by(username=form.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já solicitou acesso.")
    novo = Usuario(username=form.username, senha=form.password, status="pendente")
    db.add(novo)
    db.commit()
    return {"mensagem": "Solicitação de acesso registrada. Aguarde avaliação."}

@router.post("/avaliar-acesso")
def avaliar_acesso(username: str, status_aprovacao: str, admin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if admin.username != ADMIN_USERNAME or admin.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Acesso negado ao avaliador.")
    if status_aprovacao not in ["aprovado", "rejeitado"]:
        raise HTTPException(status_code=400, detail="Status deve ser 'aprovado' ou 'rejeitado'.")

    usuario = db.query(Usuario).filter_by(username=username).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    usuario.status = status_aprovacao
    if status_aprovacao == "aprovado":
        token = create_access_token(data={"sub": usuario.username})
        usuario.ultimo_token = token
        usuario.data_token = datetime.utcnow()
    db.commit()
    return {"mensagem": f"Usuário {username} foi {status_aprovacao}."}

@router.post("/status-acesso")
def status_acesso(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(username=form.username).first()
    if not usuario or usuario.senha != form.password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    if usuario.status == "pendente":
        return {"status": "pendente", "mensagem": "Sua solicitação ainda não foi avaliada."}
    elif usuario.status == "rejeitado":
        return {"status": "rejeitado", "mensagem": "Sua solicitação foi recusada."}
    elif usuario.status == "aprovado":
        if not usuario.ultimo_token or usuario.data_token + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) < datetime.utcnow():
            token = create_access_token(data={"sub": usuario.username})
            usuario.ultimo_token = token
            usuario.data_token = datetime.utcnow()
            db.commit()
        return {
            "status": "aprovado",
            "access_token": usuario.ultimo_token,
            "token_type": "bearer"
        }