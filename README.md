# RepositorioDesarrollo

A professional three-layer architecture FastAPI application following Clean Code principles and Feature-Driven Development.

## 📁 Project Structure

```
RepositorioDesarrollo/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── models/                   # Domain entities
│   │   ├── __init__.py
│   │   ├── base_model.py         # BaseEntity generic class
│   │   └── user.py               # User domain model
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── base_service.py       # Generic CRUD service
│   │   └── user_service.py       # User business logic
│   ├── controllers/              # HTTP endpoints layer
│   │   ├── __init__.py
│   │   └── user_routes.py        # User API routes (7 endpoints)
│   ├── schemas/                  # Pydantic validation schemas
│   │   ├── __init__.py
│   │   └── user_schemas.py       # User request/response schemas
│   └── core/                     # Core configuration
│       ├── __init__.py
│       ├── config.py             # Application settings
│       ├── exceptions.py         # Custom exceptions
│       └── utils.py              # Utility functions
├── tests/                        # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_models.py            # Unit tests for models (7 tests)
│   ├── test_services.py          # Unit tests for services (8 tests)
│   └── test_api.py               # Integration tests (12 tests)
├── docs/                         # Documentation
│   ├── 01_START_HERE.md          # 5-minute quick start (Spanish)
│   ├── 02_QUICK_START.md         # 400+ line comprehensive guide
│   ├── 03_ARCHITECTURE.md        # 500+ line technical documentation
│   └── 04_STRUCTURE_SUMMARY.md   # Architecture summary & statistics
├── scripts/                      # Utility scripts
│   └── run.py                    # FastAPI application launcher
├── config/                       # Configuration files
│   ├── .env.example              # Environment variables template
│   └── requirements.txt          # Python dependencies
├── .vscode/                      # VS Code settings
│   ├── settings.json             # Editor & Python configuration
│   ├── extensions.json           # Recommended extensions
│   └── launch.json               # Debug configurations
├── pyproject.toml                # Python project configuration
├── repositoriodesarrollo.toml    # Additional project config
├── RepositorioDesarrollo.code-workspace  # VS Code workspace
├── .python-version               # Python version specification
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Set Up Environment

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd RepositorioDesarrollo

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r config/requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp config/.env.example .env

# Edit .env with your settings
```

### 3. Run the Application

```bash
# Using the run script
python scripts/run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentation

For detailed information, see:

- **[START HERE](docs/01_START_HERE.md)** - 5-minute quick start guide (Spanish)
- **[Quick Start Guide](docs/02_QUICK_START.md)** - Comprehensive setup and usage guide
- **[Architecture](docs/03_ARCHITECTURE.md)** - Technical architecture and design patterns
- **[Structure Summary](docs/04_STRUCTURE_SUMMARY.md)** - Project structure overview

## 🏗️ Architecture

This project implements a **three-layer architecture**:

```
HTTP Requests
    ↓
┌─────────────────────────────┐
│  Controllers (Routes)       │  ← API endpoints, validation
│  user_routes.py             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Services (Business Logic)  │  ← Core logic, processing
│  user_service.py            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Models (Domain Entities)   │  ← Data representation
│  user.py                    │
└─────────────────────────────┘
```

### Key Features

- **Generic Base Classes**: `BaseEntity` and `BaseService<T>` for reusability
- **Pydantic Validation**: Type-safe request/response schemas
- **Clean Code**: KISS, DRY, YAGNI, SOLID principles
- **Comprehensive Tests**: 27 tests covering models, services, and endpoints
- **Professional Structure**: Organized directories following best practices

## 🧪 API Endpoints

### User Endpoints

```
GET    /api/users              - Get all users
POST   /api/users              - Create new user
GET    /api/users/{user_id}    - Get user by ID
PUT    /api/users/{user_id}    - Update user
DELETE /api/users/{user_id}    - Delete user
POST   /api/users/{user_id}/activate    - Activate user
POST   /api/users/{user_id}/deactivate  - Deactivate user
```

## 🛠️ Technologies & Tools

- **Framework**: FastAPI
- **Validation**: Pydantic
- **Testing**: pytest
- **Code Quality**: Ruff, Black
- **Python Version**: 3.10+
- **Editor**: Visual Studio Code with Python extension

## 📋 Development Principles

- **Clean Code**: KISS, DRY, YAGNI, SOLID
- **TDD**: Test-Driven Development
- **FDD**: Feature-Driven Development
- **Architecture**: Three-layer MVC pattern

## 🔧 VS Code Integration

This project includes VS Code configuration for:

- Python formatting with Ruff
- Pytest integration
- Debug launch configurations
- Recommended extensions

Open `.vscode/settings.json` to view editor settings.

## 📝 Original Project Goals

- Extract text from PDFs
- Summarize using AI models (Gemini)
- Professional three-layer architecture
- Clean code principles
- Comprehensive documentation

## 🤝 Contributing

When adding new features:

1. Create a new branch
2. Follow the three-layer architecture
3. Add unit and integration tests
4. Update documentation
5. Submit a pull request

## 📄 License

This is a development project. Check `LICENSE` file for details.

## 📞 Support

For more information, see the documentation in the `docs/` directory or check the code comments.

---

**Last Updated**: April 1, 2026
**Python Version**: 3.10+
**Status**: Active Development
