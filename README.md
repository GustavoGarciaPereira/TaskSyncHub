
# API de Gerenciamento de Tarefas (To-Do List)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)

## Descrição do Projeto

Esta é uma API RESTful simples para gerenciamento de uma lista de tarefas (To-Do List), desenvolvida em Python utilizando o framework FastAPI. O projeto foi criado como um teste para avaliar a proficiência em desenvolvimento de APIs, boas práticas de codificação, autenticação simples e integração com banco de dados.

## Tecnologias Utilizadas

-   **Python 3.10+**
-   **FastAPI**: Framework web para a construção da API.
-   **Uvicorn**: Servidor ASGI para executar a aplicação.
-   **PostgreSQL**: Banco de dados relacional para persistência dos dados.
-   **SQLAlchemy**: ORM para interação com o banco de dados.
-   **Pydantic**: Para validação e serialização de dados.

## Funcionalidades

-   **Operações CRUD completas** para tarefas (Criar, Ler, Atualizar, Deletar).
-   **Autenticação Simples** baseada em um token estático enviado via header HTTP.
-   **Validação de Dados** de entrada para garantir a integridade das requisições.
-   **Estrutura de Projeto Modularizada**, separando rotas, lógica de negócio e modelos.
-   **Documentação de API automática** via Swagger UI e ReDoc.

## Estrutura do Projeto

```
TaskSyncHub/
├── app/
│   ├── __init__.py
│   ├── main.py         # Ponto de entrada da aplicação FastAPI
│   ├── database.py     # Configuração da conexão com o PostgreSQL
│   ├── models.py       # Modelos de dados do SQLAlchemy
│   ├── schemas.py      # Esquemas Pydantic para validação
│   ├── crud.py         # Lógica de negócio (CRUD)
│   ├── dependencies.py # Dependências (autenticação)
│   └── routers/
│       ├── __init__.py
│       └── tasks.py    # Rotas da API para tarefas
├── .env                # Arquivo para variáveis de ambiente (não versionado)
├── .env.example        # Exemplo de arquivo de configuração
├── requirements.txt    # Lista de dependências Python
└── README.md           # Esta documentação
```

## Pré-requisitos

-   Python 3.10 ou superior.
-   Um servidor PostgreSQL em execução.


### Configuração do Banco de Dados com Docker (Alternativa)

Para facilitar o desenvolvimento e evitar a instalação manual do PostgreSQL, recomendamos o uso de Docker. Se você tem o Docker e o Docker Compose instalados, pode criar e executar um contêiner com um único comando.

**1. Execute o Contêiner do PostgreSQL**

Abra seu terminal e execute o seguinte comando. Ele fará o download da imagem oficial do PostgreSQL (se ainda não a tiver) e iniciará um contêiner pronto para uso.

```bash
docker run --rm --name postgres-container \
-e POSTGRES_USER=user \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=dbname \
-p 5432:5432 \
-v pg_data:/var/lib/postgresql/data \
postgres:16
```

**2. Entendendo o Comando**

Vamos detalhar o que cada parte do comando faz:

-   `docker run`: Inicia um novo contêiner.
-   `--rm`: Instrui o Docker a remover o contêiner automaticamente quando ele for parado. Ótimo para limpeza em ambiente de desenvolvimento.
-   `--name postgres-container`: Define um nome fácil de lembrar para o contêiner.
-   `-e POSTGRES_USER=user`: Cria um superusuário no banco chamado `user`.
-   `-e POSTGRES_PASSWORD=password`: Define a senha para o superusuário como `password`.
-   `-e POSTGRES_DB=dbname`: Cria um banco de dados inicial chamado `dbname`.
-   `-p 5432:5432`: Mapeia a porta `5432` do seu computador (host) para a porta `5432` do contêiner. É isso que permite que sua API (rodando no host) se conecte ao banco (rodando no contêiner).
-   `-v pg_data:/var/lib/postgresql/data`: Cria um **volume nomeado** chamado `pg_data`. Isso garante que os dados do seu banco de dados **sejam persistidos** no seu computador, mesmo que o contêiner seja parado ou removido.
-   `postgres:16`: Especifica a imagem Docker a ser usada.

**3. Conectando a API ao Banco Docker**

Após executar o comando acima, seu banco de dados estará acessível. Certifique-se de que seu arquivo `.env` (na raiz do projeto da API) corresponda exatamente a essas configurações:

```ini
# .env
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${POSTGRES_DB}"
API_TOKEN="mysecrettoken"
```

**4. Gerenciando o Contêiner**

Você pode gerenciar o contêiner com os seguintes comandos:

-   **Para parar o contêiner:**
    ```bash
    docker stop postgres-container
    ```
-   **Para iniciar o contêiner novamente (se não usou `--rm`):**
    ```bash
    docker start postgres-container
    ```
-   **Para ver os logs do banco de dados:**
    ```bash
    docker logs -f postgres-container
    ```


## Configuração com Docker Compose

Para facilitar o desenvolvimento e implantação, o projeto inclui um arquivo `docker-compose.yml` que configura automaticamente:

1. **Serviço PostgreSQL** (banco de dados)
2. **Serviço FastAPI** (aplicação)

### Como usar:

1. **Certifique-se de ter o Docker e Docker Compose instalados**

2. **Configure o arquivo `.env`** (na raiz do projeto) com as seguintes variáveis:

```ini
# Configurações do PostgreSQL
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname

# Configuração da API
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${POSTGRES_DB}"
API_TOKEN=mysecrettoken
```

3. **Execute o sistema com um único comando:**

```bash
docker-compose up --build
```

### Serviços Configurados:

#### 1. Banco de Dados PostgreSQL (`db`)
- **Imagem:** `postgres:16`
- **Porta:** 5432 (mapeada para localhost)
- **Volume persistente:** `pg_data` (dados não são perdidos ao reiniciar)
- **Healthcheck:** Verifica automaticamente se o banco está pronto

#### 2. Aplicação FastAPI (`api`)
- **Build:** Usa o Dockerfile do projeto
- **Porta:** 8000 (mapeada para localhost)
- **Live-reload:** Código montado do diretório local (`./app`)
- **Dependência:** Só inicia após o banco estar saudável

### Comandos úteis:

| Comando | Descrição |
|---------|-----------|
| `docker-compose up --build` | Inicia os serviços e reconstrói as imagens |
| `docker-compose up -d` | Executa em segundo plano |
| `docker-compose down` | Para e remove os containers |
| `docker-compose logs -f` | Mostra logs em tempo real |
| `docker-compose restart api` | Reinicia apenas o serviço da API |

### Acessando a API:

Após iniciar os containers, a API estará disponível em:
- **Local:** `http://localhost:8000`
- **Documentação:** `http://localhost:8000/docs`

### Observações:
- O volume `pg_data` mantém os dados do PostgreSQL entre execuções
- Modificações no código (`./app`) refletem automaticamente no container
- Para desenvolvimento, use `--build` após fazer alterações no Dockerfile

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto localmente.

**1. Clone o Repositório**
```bash
git clone https://github.com/GustavoGarciaPereira/TaskSyncHub.git
cd TaskSyncHub
```

**2. Crie e Ative um Ambiente Virtual**
```bash
# Para Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Instale as Dependências**
```bash
pip install -r requirements.txt
```
*(Nota: Crie um arquivo `requirements.txt` com o comando `pip freeze > requirements.txt` após instalar as bibliotecas: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`)*

**4. Configure as Variáveis de Ambiente**

Crie um arquivo chamado `.env` na raiz do projeto, copiando o conteúdo de `.env.example`:

```bash
cp .env.example .env
```

Agora, edite o arquivo `.env` com as suas credenciais do PostgreSQL e o token desejado:

```ini
# .env
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${POSTGRES_DB}"
API_TOKEN="mysecrettoken"
```

## Execução

Para iniciar a aplicação, execute o seguinte comando na raiz do projeto:

```bash
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`. A opção `--reload` reinicia o servidor automaticamente após qualquer alteração no código.

## Uso da API (Endpoints)

**Token de Autenticação:** Todas as rotas protegidas exigem o envio do token no header da requisição:
`token: mysecrettoken`

---

### 1. Criar uma Nova Tarefa

-   **Método:** `POST`
-   **Endpoint:** `/tasks/`
-   **Descrição:** Cria uma nova tarefa.
-   **Exemplo com `curl`:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/tasks/" \
    -H "Content-Type: application/json" \
    -H "token: mysecrettoken" \
    -d '{
      "title": "Estudar FastAPI",
      "description": "Criar um projeto CRUD completo."
    }'
    ```
-   **Resposta de Sucesso (201 Created):**
    ```json
    {
      "id": 1,
      "title": "Estudar FastAPI",
      "description": "Criar um projeto CRUD completo."
    }
    ```

---

### 2. Listar Todas as Tarefas

-   **Método:** `GET`
-   **Endpoint:** `/tasks/`
-   **Descrição:** Retorna uma lista de todas as tarefas.
-   **Exemplo com `curl`:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/tasks/" \
    -H "token: mysecrettoken"
    ```
-   **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "id": 1,
        "title": "Estudar FastAPI",
        "description": "Criar um projeto CRUD completo."
      }
    ]
    ```

---

### 3. Obter uma Tarefa Específica

-   **Método:** `GET`
-   **Endpoint:** `/tasks/{task_id}`
-   **Descrição:** Retorna os detalhes de uma tarefa específica pelo seu ID.
-   **Exemplo com `curl`:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/tasks/1" \
    -H "token: mysecrettoken"
    ```
-   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "id": 1,
      "title": "Estudar FastAPI",
      "description": "Criar um projeto CRUD completo."
    }
    ```

---

### 4. Atualizar uma Tarefa

-   **Método:** `PUT`
-   **Endpoint:** `/tasks/{task_id}`
-   **Descrição:** Atualiza os dados de uma tarefa existente.
-   **Exemplo com `curl`:**
    ```bash
    curl -X PUT "http://127.0.0.1:8000/tasks/1" \
    -H "Content-Type: application/json" \
    -H "token: mysecrettoken" \
    -d '{
      "title": "Estudar FastAPI - Concluído",
      "description": "O projeto CRUD foi finalizado com sucesso."
    }'
    ```
-   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "id": 1,
      "title": "Estudar FastAPI - Concluído",
      "description": "O projeto CRUD foi finalizado com sucesso."
    }
    ```

---

### 5. Excluir uma Tarefa

-   **Método:** `DELETE`
-   **Endpoint:** `/tasks/{task_id}`
-   **Descrição:** Remove uma tarefa do banco de dados.
-   **Exemplo com `curl`:**
    ```bash
    curl -X DELETE "http://127.0.0.1:8000/tasks/1" \
    -H "token: mysecrettoken"
    ```
-   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "id": 1,
      "title": "Estudar FastAPI - Concluído",
      "description": "O projeto CRUD foi finalizado com sucesso."
    }
    ```

### 6. Testes
Na Raiz do projeto tode o comando 
```bash
pytest tests/test_tasks.py -v --cov=app --cov-report=term-missing  
```
resultado esperado
```bash
pytest tests/test_tasks.py -v --cov=app --cov-report=term-missing                                                                                 main  
========================================================================================== test session starts ==========================================================================================
platform linux -- Python 3.12.7, pytest-8.4.1, pluggy-1.6.0 -- /home/gustavo/TaskSyncHub/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/gustavo/TaskSyncHub
configfile: pytest.ini
plugins: cov-6.2.1, anyio-4.9.0
collected 13 items                                                                                                                                                                                      

tests/test_tasks.py::test_create_task_success PASSED                                                                                                                                              [  7%]
tests/test_tasks.py::test_create_task_with_empty_title PASSED                                                                                                                                     [ 15%]
tests/test_tasks.py::test_create_task_with_null_description PASSED                                                                                                                                [ 23%]
tests/test_tasks.py::test_create_task_database_error PASSED                                                                                                                                       [ 30%]
tests/test_tasks.py::test_create_task_unexpected_error PASSED                                                                                                                                     [ 38%]
tests/test_tasks.py::test_get_tasks_success PASSED                                                                                                                                                [ 46%]
tests/test_tasks.py::test_get_tasks_with_invalid_limit PASSED                                                                                                                                     [ 53%]
tests/test_tasks.py::test_get_task_success PASSED                                                                                                                                                 [ 61%]
tests/test_tasks.py::test_get_task_not_found PASSED                                                                                                                                               [ 69%]
tests/test_tasks.py::test_update_task_success PASSED                                                                                                                                              [ 76%]
tests/test_tasks.py::test_update_task_not_found PASSED                                                                                                                                            [ 84%]
tests/test_tasks.py::test_delete_task_success PASSED                                                                                                                                              [ 92%]
tests/test_tasks.py::test_delete_task_database_error_on_commit PASSED                                                                                                                             [100%]

============================================================================================ tests coverage =============================================================================================
____________________________________________________________________________ coverage: platform linux, python 3.12.7-final-0 ____________________________________________________________________________

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py             0      0   100%
app/crud.py               117     33    72%   78, 96-104, 129, 143-144, 149-150, 157-159, 185, 189, 207-210, 218-219, 226-228, 253, 259, 278-279, 286-288
app/database.py            14      4    71%   19-23
app/dependencies.py         8      8     0%   1-17
app/logging_config.py      12     12     0%   1-50
app/main.py                12     12     0%   1-15
app/models.py              11      1    91%   14
app/schemas.py             11      0   100%
app/services.py             0      0   100%
-----------------------------------------------------
TOTAL                     185     70    62%
========================================================================================== 13 passed in 2.50s ===========================================================================================
```
caso esteja queira usar direto o comainer
```bash
# Testes básicos
docker-compose run --rm tests python -m pytest /app/tests/test_tasks.py -v

# Com cobertura (opcional)
docker-compose run --rm tests python -m pytest /app/tests/test_tasks.py -v --cov=/app/app --cov-report=term-missing
```

## Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa da API. Após iniciar o servidor, você pode acessá-la nos seguintes endereços:

-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc`