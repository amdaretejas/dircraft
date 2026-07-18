from typing import Dict, Optional


def build_python_dev_structure(name: str) -> Dict[str, Optional[str]]:
    """Full-stack (FastAPI backend + Streamlit frontend) dev scaffold."""
    root = name

    files: Dict[str, Optional[str]] = {}

    # ---- root-level files -------------------------------------------------
    files[f"{root}/.gitignore"] = _gitignore()
    files[f"{root}/.env"] = _env(name)
    files[f"{root}/.env.example"] = _env(name)
    files[f"{root}/.editorconfig"] = _editorconfig()
    files[f"{root}/docker-compose.yml"] = _docker_compose(name)
    files[f"{root}/README.md"] = _root_readme(name)

    # ---- backend (FastAPI) -------------------------------------------------
    b = f"{root}/backend"
    files[f"{b}/requirements.txt"] = _backend_requirements()
    files[f"{b}/Dockerfile"] = _backend_dockerfile()

    files[f"{b}/app/__init__.py"] = ""
    files[f"{b}/app/main.py"] = _backend_main(name)

    files[f"{b}/app/api/__init__.py"] = ""
    files[f"{b}/app/api/deps.py"] = _backend_api_deps()
    files[f"{b}/app/api/v1/__init__.py"] = ""
    files[f"{b}/app/api/v1/router.py"] = _backend_api_router()
    files[f"{b}/app/api/v1/routes/__init__.py"] = ""
    files[f"{b}/app/api/v1/routes/health.py"] = _backend_route_health()
    files[f"{b}/app/api/v1/routes/auth.py"] = _backend_route_auth()
    files[f"{b}/app/api/v1/routes/users.py"] = _backend_route_users()

    files[f"{b}/app/core/__init__.py"] = ""
    files[f"{b}/app/core/config.py"] = _backend_core_config(name)
    files[f"{b}/app/core/security.py"] = _backend_core_security()
    files[f"{b}/app/core/logging.py"] = _backend_core_logging()

    files[f"{b}/app/db/__init__.py"] = ""
    files[f"{b}/app/db/base.py"] = _backend_db_base()
    files[f"{b}/app/db/session.py"] = _backend_db_session()

    files[f"{b}/app/models/__init__.py"] = ""
    files[f"{b}/app/models/user.py"] = _backend_model_user()

    files[f"{b}/app/schemas/__init__.py"] = ""
    files[f"{b}/app/schemas/user.py"] = _backend_schema_user()

    files[f"{b}/app/services/__init__.py"] = ""
    files[f"{b}/app/services/user_service.py"] = _backend_service_user()

    files[f"{b}/app/utils/__init__.py"] = ""
    files[f"{b}/app/utils/helpers.py"] = _backend_utils_helpers()

    files[f"{b}/app/middleware/__init__.py"] = ""
    files[f"{b}/app/middleware/auth_middleware.py"] = _backend_middleware_auth()

    files[f"{b}/tests/__init__.py"] = ""
    files[f"{b}/tests/conftest.py"] = _backend_tests_conftest()
    files[f"{b}/tests/test_health.py"] = _backend_tests_health()

    files[f"{b}/scripts/seed_data.py"] = _backend_scripts_seed()

    # ---- frontend (Streamlit) ----------------------------------------------
    f = f"{root}/frontend"
    files[f"{f}/requirements.txt"] = _frontend_requirements()
    files[f"{f}/Dockerfile"] = _frontend_dockerfile()
    files[f"{f}/.gitignore"] = _frontend_gitignore()
    files[f"{f}/.streamlit/config.toml"] = _frontend_streamlit_config()
    files[f"{f}/.streamlit/secrets.toml.example"] = _frontend_streamlit_secrets_example()
    files[f"{f}/main.py"] = _frontend_main(name)
    files[f"{f}/services/__init__.py"] = ""
    files[f"{f}/services/api_client.py"] = _frontend_api_client()
    files[f"{f}/pages/1_Example.py"] = _frontend_example_page()

    return files


# ---------------------------------------------------------------------------
# root-level file contents
# ---------------------------------------------------------------------------

def _gitignore() -> str:
    return """# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.egg
build/
dist/
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# Environment
.env
.env.local

# Frontend / Streamlit
frontend/.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3
"""


def _env(name: str) -> str:
    return f"""PROJECT_NAME={name}
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=change-me
DATABASE_URL=sqlite:///./app.db

# Used by the frontend to reach the backend.
# docker-compose sets this to http://backend:8000/api/v1 automatically.
API_BASE_URL=http://localhost:8000/api/v1
"""


def _editorconfig() -> str:
    return """root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
"""


def _docker_compose(name: str) -> str:
    return f"""version: "3.9"

services:
  backend:
    build: ./backend
    container_name: {name}_backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    container_name: {name}_frontend
    ports:
      - "8501:8501"
    env_file:
      - .env
    environment:
      - API_BASE_URL=http://backend:8000/api/v1
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
"""


def _root_readme(name: str) -> str:
    return f"""# {name}

Full-stack project scaffolded with [dircraft](https://pypi.org/project/dircraft/).

## Structure

- `backend/` — FastAPI service (`app/main.py`)
- `frontend/` — Streamlit app (`main.py`)

## Run with Docker

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:8501

## Run locally

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
pip install -r requirements.txt
streamlit run main.py
```
"""


# ---------------------------------------------------------------------------
# backend file contents
# ---------------------------------------------------------------------------

def _backend_requirements() -> str:
    return """fastapi
uvicorn[standard]
pydantic-settings
sqlalchemy
python-jose[cryptography]
passlib[bcrypt]
pytest
httpx
"""


def _backend_dockerfile() -> str:
    return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
"""


def _backend_main(name: str) -> str:
    return f"""from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {{"message": f"{{settings.PROJECT_NAME}} is running"}}
"""


def _backend_api_deps() -> str:
    return """from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""


def _backend_api_router() -> str:
    return """from fastapi import APIRouter

from app.api.v1.routes import auth, health, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
"""


def _backend_route_health() -> str:
    return """from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}
"""


def _backend_route_auth() -> str:
    return """from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    return {"message": "login endpoint"}
"""


def _backend_route_users() -> str:
    return """from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_users():
    return []
"""


def _backend_core_config(name: str) -> str:
    return f"""from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "{name}"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"
    DATABASE_URL: str = "sqlite:///./app.db"


settings = Settings()
"""


def _backend_core_security() -> str:
    return """from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
"""


def _backend_core_logging() -> str:
    return """import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
"""


def _backend_db_base() -> str:
    return """from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""


def _backend_db_session() -> str:
    return """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""


def _backend_model_user() -> str:
    return """from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
"""


def _backend_schema_user() -> str:
    return """from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
"""


def _backend_service_user() -> str:
    return """from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
"""


def _backend_utils_helpers() -> str:
    return """def to_camel_case(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(word.title() for word in parts[1:])
"""


def _backend_middleware_auth() -> str:
    return """from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)
"""


def _backend_tests_conftest() -> str:
    return """import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
"""


def _backend_tests_health() -> str:
    return """def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
"""


def _backend_scripts_seed() -> str:
    return """def seed() -> None:
    print("Seeding database...")


if __name__ == "__main__":
    seed()
"""


# ---------------------------------------------------------------------------
# frontend (Streamlit) file contents
# ---------------------------------------------------------------------------

def _frontend_requirements() -> str:
    return """streamlit
requests
"""


def _frontend_dockerfile() -> str:
    return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""


def _frontend_gitignore() -> str:
    return """__pycache__/
.streamlit/secrets.toml
"""


def _frontend_streamlit_config() -> str:
    return """[server]
port = 8501
headless = true

[theme]
primaryColor = "#4F8BF9"
"""


def _frontend_streamlit_secrets_example() -> str:
    return """# Copy this file to secrets.toml and fill in real values.
# secrets.toml is gitignored and must never be committed.
api_base_url = "http://localhost:8000/api/v1"
"""


def _frontend_main(name: str) -> str:
    return f"""import streamlit as st

from services.api_client import get_health

st.set_page_config(page_title="{name}", layout="wide")
st.title("{name}")
st.caption("Frontend is running")

if st.button("Check backend health"):
    try:
        st.success(get_health())
    except Exception as exc:
        st.error(f"Backend unreachable: {{exc}}")
"""


def _frontend_api_client() -> str:
    return """import os

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


def get_health() -> dict:
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
    response.raise_for_status()
    return response.json()
"""


def _frontend_example_page() -> str:
    return """import streamlit as st

st.title("Example Page")
st.write("This is an example additional Streamlit page.")
"""
