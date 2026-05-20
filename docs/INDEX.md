# Documentation Index

Welcome to the RepositorioDesarrollo documentation. This is a Python FastAPI project for managing PDF documents with MongoDB backend.

## 🚀 Quick Navigation

### For Getting Started
Start here if you're new to the project:
1. **[README.md](../README.md)** - Main project overview and setup
2. **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** - Complete Spanish guide

### For Development References
1. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - Implementation tasks and progress
2. **[bibliotecas.md](bibliotecas.md)** - Project dependencies and libraries
3. **[CLEAN_CODE_VERIFICATION.md](CLEAN_CODE_VERIFICATION.md)** - Code quality checklist
4. **[CLEAN_CODE_FIXES.md](CLEAN_CODE_FIXES.md)** - Applied clean code improvements

---

## 📚 Complete Documentation Breakdown

### GUIA_COMPLETA.md
- **Audience**: All developers, comprehensive Spanish guide
- **Contains**:
  - Project overview and purpose
  - Architecture and structure explanation
  - Setup and installation instructions
  - How to run the application
  - Testing guide
  - API documentation
  - Development guidelines

### IMPLEMENTATION_CHECKLIST.md
- **Audience**: Developers and project managers
- **Contains**:
  - Task list for implementation progress
  - Feature checklist
  - Testing requirements
  - Documentation status

### bibliotecas.md
- **Audience**: All developers
- **Contains**:
  - Complete list of project dependencies
  - Library descriptions and versions
  - Purpose of each external package

### CLEAN_CODE_VERIFICATION.md
- **Audience**: Code reviewers, senior developers
- **Contains**:
  - Code quality standards checklist
  - Clean Code principles verification
  - Architecture compliance checks
  - Testing coverage requirements

### CLEAN_CODE_FIXES.md
- **Audience**: All developers
- **Contains**:
  - Summary of applied clean code improvements
  - Refactoring changes made
  - Best practices implemented

---

## 🎯 Project Structure Overview

```
├── app/                          # Main application code
│   ├── main.py                  # FastAPI application entry point
│   ├── controllers/             # API route handlers
│   │   ├── pdf_routes.py       # PDF management endpoints
│   │   └── user_routes.py      # User management endpoints
│   ├── core/                   # Core functionality
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # MongoDB connection
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── mongo_repository.py # MongoDB operations
│   │   ├── repository.py       # Base repository pattern
│   │   ├── utils.py            # Utility functions
│   │   └── middleware/         # HTTP middleware
│   ├── models/                 # Data models
│   │   ├── base_model.py       # Base model class
│   │   └── pdf_document.py     # PDF document model
│   ├── schemas/                # Pydantic schemas
│   │   └── pdf_schemas.py      # PDF validation schemas
│   └── services/               # Business logic
│       ├── base_service.py     # Base service class
│       └── pdf_service.py      # PDF operations service
├── config/                      # Configuration files
│   ├── repositoriodesarrollo.toml
│   └── requirements.txt        # Python dependencies
├── docs/                        # Documentation (this folder)
├── scripts/                     # Utility scripts
│   └── run.py                  # Application launcher
├── tests/                       # Test suite
│   ├── test_pdfs.py           # PDF functionality tests
├── pyproject.toml              # Python project configuration
├── docker-compose.yml          # Docker Compose setup
└── README.md                   # Main project README
```

## 📋 Key Technologies

- **Framework**: FastAPI
- **Database**: MongoDB
- **Language**: Python 3.x
- **Package Management**: Poetry (pyproject.toml)
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

---

## 🔗 Additional Resources

### Root Files
- `README.md` - Main project documentation
- `pyproject.toml` - Python project and dependency configuration
- `docker-compose.yml` - Container orchestration
- `diagrama.puml` - Project diagram (PlantUML)
- `validate_fixes.py` - Validation script

### Configuration
See `config/` directory for:
- `requirements.txt` - Python package dependencies
- `repositoriodesarrollo.toml` - Project-specific configuration

### Scripts
See `scripts/` directory for:
- `run.py` - Application launcher and runner

### Testing
See `tests/` directory for:
- `test_pdfs.py` - PDF functionality unit tests

---

## 🎯 Choose Your Path

**I just got the repository:**
→ Read [README.md](../README.md) for quick setup

**I want a complete guide (Spanish):**
→ Read [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

**I need to know what to implement:**
→ Check [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)

**I need to understand project dependencies:**
→ See [bibliotecas.md](bibliotecas.md)

**I'm doing code review:**
→ Use [CLEAN_CODE_VERIFICATION.md](CLEAN_CODE_VERIFICATION.md)

**I want to see what was improved:**
→ Read [CLEAN_CODE_FIXES.md](CLEAN_CODE_FIXES.md)
- `settings.json` - Editor configuration
- `extensions.json` - Recommended extensions
- `launch.json` - Debug configurations

---

## 📞 Questions?

If documentation is unclear:
1. Check the relevant `.md` file again (search for keywords)
2. Look at the code examples in `docs/02_QUICK_START.md`
3. Review `app/` code comments
4. Check test files in `tests/` for usage examples

---

**Last Updated**: April 1, 2026
**Project Status**: Active Development
