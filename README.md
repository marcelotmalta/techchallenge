
# Tech Challenge - API Embrapa

API desenvolvida com FastAPI para consultar dados públicos de vitivinicultura da Embrapa. Esta API servirá como base de ingestão de dados para um futuro modelo de Machine Learning.

O projeto está disponibilizado no Render através do endereço: https://techchallenge-ai7z.onrender.com/docs#/

## Como rodar localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload

```

#Estrutura do projeto
```
tech_challenge/
├──app/
├── __init__.py                     # Inicializador do pacote
├── analytics.py                    # Endpoints para análises futuras (ex: previsão, tendências)
├── auth_token.py                   # Validação de tokens JWT para proteger endpoints
├── config.py                       # Configurações globais da aplicação (secret key, expiração, etc.)
├── database.py                     # Inicialização do SQLAlchemy e conexão com SQLite
├── models.py                       # Modelos de dados SQLAlchemy (produção, usuários, etc.)
├── routes.py                       # Organização principal dos endpoints e routers
├── routes_analytics_integrado.py   # Versão completa incluindo endpoints analíticos
├── scraper.py                      # Scraper principal para produção, comercialização, processamento
├── scraper_import_export.py        # Scraper específico para importações e exportações
├── utils.py                        # Funções auxiliares como criação e validação de tokens JWT
│
├── requirements.txt          # Dependências do projeto
├── README.md                 # Instruções do projeto
├── main.py                   # comandos de inicialização do projeto
├── Procfile                  # comando de inicialização para o render
└── .gitignore                # Ignora arquivos desnecessários
```


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


### 🔐 Segurança

- Acesso controlado com fluxo de aprovação
- Tokens JWT com expiração automática
- Proteção de todos os endpoints via `Depends(get_current_user)`

---


## 🧱 Estrutura das Tabelas

Abaixo estão os principais modelos de dados utilizados no banco (via SQLAlchemy), com suas respectivas funções e campos:

---

### 📦 `producao`
Armazena dados históricos de produção de uvas por tipo de produto e ano.

| Campo              | Tipo     | Descrição                            |
|--------------------|----------|----------------------------------------|
| `id`               | Integer  | Identificador único (autoincremento)  |
| `id_original`      | Integer  | ID da fonte original do dado          |
| `control`          | String   | Identificador de controle da Embrapa  |
| `produto`          | String   | Tipo de produto vitivinícola          |
| `ano`              | Integer  | Ano da produção                       |
| `producao_toneladas` | Float | Quantidade produzida em toneladas     |

🔐 Restrição: cada `(id_original, ano)` deve ser único.

---

### 💼 `comercializacao`
Registra o volume de comercialização dos produtos vitivinícolas por ano.

| Campo                  | Tipo     | Descrição                             |
|------------------------|----------|-----------------------------------------|
| `id`                   | Integer  | Identificador único                    |
| `id_original`          | Integer  | ID da fonte original                   |
| `control`              | String   | Código de controle                     |
| `produto`              | String   | Tipo de produto                        |
| `ano`                  | Integer  | Ano da comercialização                 |
| `volume_comercializado`| Float    | Volume comercializado (litros/toneladas) |

🔐 Restrição: cada `(id_original, ano)` deve ser único.

---

### 🏭 `processamento`
Registra o volume de uvas processadas por cultivar e ano.

| Campo                    | Tipo     | Descrição                             |
|--------------------------|----------|-----------------------------------------|
| `id`                     | Integer  | Identificador único                    |
| `id_original`            | Integer  | ID da fonte original                   |
| `control`                | String   | Código de controle                     |
| `cultivar`               | String   | Tipo da uva                            |
| `ano`                    | Integer  | Ano do processamento                   |
| `volume_processado_litros` | Float  | Volume processado em litros            |

🔐 Restrição: cada `(id_original, ano)` deve ser único.

---

### 🌎 `importacao`
Contém dados de importação de vinhos por país e ano.

| Campo         | Tipo     | Descrição                              |
|---------------|----------|------------------------------------------|
| `id`          | Integer  | Identificador único                     |
| `pais`        | String   | Nome do país de origem                  |
| `ano`         | Integer  | Ano da importação                       |
| `quantidade`  | Float    | Quantidade importada                   |
| `valor_usd`   | Float    | Valor total em dólares                 |

🔐 Restrição: cada `(pais, ano)` deve ser único.

---

### 🌍 `exportacao`
Semelhante à `importacao`, mas referente às exportações por país e ano.

| Campo         | Tipo     | Descrição                              |
|---------------|----------|------------------------------------------|
| `id`          | Integer  | Identificador único                     |
| `pais`        | String   | Nome do país de destino                 |
| `ano`         | Integer  | Ano da exportação                       |
| `quantidade`  | Float    | Quantidade exportada                   |
| `valor_usd`   | Float    | Valor total em dólares                 |

🔐 Restrição: cada `(pais, ano)` deve ser único.

---

### 👤 `usuarios`
Controla os acessos à API via autenticação com aprovação por administrador.

| Campo          | Tipo     | Descrição                              |
|----------------|----------|------------------------------------------|
| `id`           | Integer  | Identificador único                    |
| `username`     | String   | Nome do usuário                        |
| `senha`        | String   | Senha do usuário                       |
| `status`       | String   | `pendente`, `aprovado` ou `rejeitado` |
| `ultimo_token` | String   | Último token gerado (JWT)              |
| `data_token`   | DateTime | Data da última geração de token        |


---

### 🔮 Escalabilidade futura

- Já estruturado para receber modelos de previsão (ML)
- Modularidade para substituição de SQLite por PostgreSQL
- Suporte a deploy em nuvem com Docker ou Vercel


## 🔮 Funcionalidades futuras planejadas

A API está estruturada para expansão futura com inteligência analítica, incluindo:

| Endpoint                                       | Descrição                                                                 |
|------------------------------------------------|---------------------------------------------------------------------------|
| `/analytics/producao/previsao`                | Previsão da produção de uvas com base em séries históricas               |
| `/analytics/exportacao/tendencias`            | Análise de tendências de exportação por país                             |
| `/analytics/comercializacao/ranking-regioes`  | Classificação de regiões por volume de comercialização                   |
| `/analytics/importacao/alerta-estoque`        | Recomendação de ajuste de estoque com base na previsão de importação     |

Esses endpoints estão documentados e estruturados, prontos para integração com modelos de machine learning ou algoritmos estatísticos conforme evolução do projeto.
