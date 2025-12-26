# MakeFolder
this is a simple lib to build entire folder structer

# - pip install dircraft


backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependencies (auth, db session)
│   │   ├── v1/                  # API versioning
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── roles.py
│   │   │   │   ├── products.py
│   │   │   │   └── health.py
│   │   │   └── router.py        # Central router for v1
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Environment & settings
│   │   ├── security.py          # JWT, hashing, OAuth
│   │   ├── logging.py           # Central logging config
│   │   └── constants.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py              # Base model
│   │   ├── session.py           # DB session handling
│   │   ├── init_db.py           # DB initialization
│   │   └── migrations/          # Alembic migrations
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   └── product.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py              # Pydantic schemas
│   │   ├── auth.py
│   │   └── product.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Business logic
│   │   ├── user_service.py
│   │   └── product_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── hashing.py
│   │   ├── tokens.py
│   │   └── helpers.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   └── rate_limit.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_users.py
│       └── conftest.py
│
├── scripts/
│   ├── create_superuser.py
│   └── seed_data.py
│
├── .env
├── .env.example
├── requirements.txt
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── README.md
