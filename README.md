
# Tech Challenge - API Embrapa

API desenvolvida com FastAPI para consultar dados públicos de vitivinicultura da Embrapa. Esta API servirá como base de ingestão de dados para um futuro modelo de Machine Learning.

## Como rodar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

```

#Estrutura do projeto
tech_challenge/
app/
├── __init__.py                     # Inicializador do pacote
├── analytics.py                    # Endpoints para análises futuras (ex: previsão, tendências)
├── auth_extended.py                # Lógica de autenticação via JWT com fluxo de aprovação
├── auth_token.py                   # Validação de tokens JWT para proteger endpoints
├── config.py                       # Configurações globais da aplicação (secret key, expiração, etc.)
├── database.py                     # Inicialização do SQLAlchemy e conexão com SQLite
├── models.py                       # Modelos de dados SQLAlchemy (produção, usuários, etc.)
├── routes.py                       # Organização principal dos endpoints e routers
├── routes_protegido_jwt.py         # Versão alternativa com autenticação em todos os GETs
├── routes_com_auth_extendido.py    # Versão alternativa com rotas de autenticação estendida
├── routes_analytics_integrado.py   # Versão completa incluindo endpoints analíticos
├── scraper.py                      # Scraper principal para produção, comercialização, processamento
├── scraper_import_export.py        # Scraper específico para importações e exportações
├── utils.py                        # Funções auxiliares como criação e validação de tokens JWT
│
├── requirements.txt          # Dependências do projeto
├── README.md                 # Instruções do projeto
└── .gitignore                # Ignora arquivos desnecessários



## 🧭 Plano Arquitetural do Projeto

Este projeto foi estruturado com foco em modularidade, escalabilidade e segurança no consumo de dados públicos do setor vitivinícola.

### 🔁 Fluxo geral de dados

```
     [ Portal Embrapa ]
           |
           v
  (1) Scraping com BeautifulSoup + requests
           |
           v
  (2) Transformação com pandas
           |
           v
  (3) Persistência com SQLAlchemy (SQLite)
           |
           v
  (4) API RESTful com FastAPI
           |
           v
  (5) Acesso com autenticação via JWT + aprovação por admin
```

---

### 🧩 Módulos e responsabilidades

| Módulo                     | Responsabilidade                                                                 |
|----------------------------|----------------------------------------------------------------------------------|
| `scraper.py`               | Coleta e transforma dados de produção, comercialização e processamento          |
| `scraper_import_export.py` | Trata arquivos com estrutura de colunas duplicadas (importação/exportação)      |
| `models.py`                | Modelos de dados com validação e restrições de unicidade via SQLAlchemy         |
| `database.py`              | Inicialização da conexão SQLite                                                 |
| `auth_extended.py`         | Fluxo de autenticação com solicitação, aprovação e geração de token JWT         |
| `auth_token.py`            | Validação e exigência de token para proteção de endpoints                       |
| `routes.py`                | Organização dos endpoints em grupos lógicos                                     |
| `analytics.py`             | Estrutura inicial para endpoints analíticos futuros (previsão, tendências etc)  |

---

### 🔐 Segurança

- Acesso controlado com fluxo de aprovação
- Tokens JWT com expiração automática
- Proteção de todos os endpoints via `Depends(get_current_user)`

---

### 🔮 Escalabilidade futura

- Já estruturado para receber modelos de previsão (ML)
- Modularidade para substituição de SQLite por PostgreSQL
- Suporte a deploy em nuvem com Docker ou Vercel


# API Vitivinícola
---

## 🔮 Funcionalidades futuras planejadas

A API está estruturada para expansão futura com inteligência analítica, incluindo:

| Endpoint                                       | Descrição                                                                 |
|------------------------------------------------|---------------------------------------------------------------------------|
| `/analytics/producao/previsao`                | Previsão da produção de uvas com base em séries históricas               |
| `/analytics/exportacao/tendencias`            | Análise de tendências de exportação por país                             |
| `/analytics/comercializacao/ranking-regioes`  | Classificação de regiões por volume de comercialização                   |
| `/analytics/importacao/alerta-estoque`        | Recomendação de ajuste de estoque com base na previsão de importação     |

Esses endpoints estão documentados e estruturados, prontos para integração com modelos de machine learning ou algoritmos estatísticos conforme evolução do projeto.