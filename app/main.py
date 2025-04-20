from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import Producao

# Criação das tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tech Challenge API - Embrapa",
    description="Consulta pública dos dados de vitivinicultura da Embrapa",
    version="1.0.0"
)

# Libera CORS se necessário
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API da Embrapa para Machine Learning - Tech Challenge"}
