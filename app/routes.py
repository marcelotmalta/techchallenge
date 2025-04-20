
from fastapi import APIRouter
from app.scraper import fetch_dados_embrapa
from app.scraper_import_export import fetch_dados_import_export

router = APIRouter()

@router.get("/producao")
def producao():
    return fetch_dados_embrapa("producao")

@router.get("/comercializacao")
def comercializacao():
    return fetch_dados_embrapa("comercializacao")

@router.get("/processamento")
def processamento():
    return fetch_dados_embrapa("processamento")

@router.get("/importacao")
def importacao():
    return fetch_dados_import_export("importacao")

@router.get("/exportacao")
def exportacao():
    return fetch_dados_import_export("exportacao")
