
# Tech Challenge - API Embrapa

API desenvolvida com FastAPI para consultar dados públicos de vitivinicultura da Embrapa. Esta API servirá como base de ingestão de dados para um futuro modelo de Machine Learning.

## Como rodar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

```

#Estrutura do projeto
tech_challenge/
│
├── app/
│   ├── main.py               # Ponto de entrada da API
│   ├── scraper.py            # Funções de scraping dos dados da Embrapa
│   ├── routes.py             # Endpoints da API
│   ├── models.py             # (Futuro) Modelos de dados (ex: Pydantic/Base de dados)
|   ├── database.py           # Conexão e base do SQLAlchemy
│   ├── utils.py              # Funções auxiliares
│   └── config.py             # Configurações gerais
│
├── requirements.txt          # Dependências do projeto
├── README.md                 # Instruções do projeto
└── .gitignore                # Ignora arquivos desnecessários
