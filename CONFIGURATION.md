# Configuration Files Reference

## Overview
This document provides a quick reference for all configuration files in the SmartCart project.

---

## 📋 Configuration Files Created/Updated

### 1. **.gitignore** ✅ UPDATED
**Purpose**: Specifies files and directories to ignore in Git
**Contents**:
- Python cache and bytecode files
- Virtual environments
- Django migrations (except __init__.py)
- IDE/Editor settings (.vscode, .idea)
- Environment variables (.env files)
- Database and media files
- Testing coverage and temporary files
- Docker and Kubernetes secrets
- OS-specific files (.DS_Store, Thumbs.db)

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/.gitignore`

---

### 2. **.env.example** ✅ CREATED
**Purpose**: Template for environment variables
**Sections**:
- Django settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- Database configuration (PostgreSQL)
- Redis and Celery settings
- Email configuration (SMTP)
- Payment gateway (Paystack, Stripe)
- AWS S3 configuration
- JWT authentication settings
- CORS settings
- Logging and error tracking
- SMS configuration (Twilio)

**Usage**: Copy to `.env` and fill in actual values
```bash
cp .env.example .env
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/.env.example`

---

### 3. **Dockerfile** ✅ CREATED
**Purpose**: Container image specification for production
**Features**:
- Base image: Python 3.10 slim
- Non-root user (appuser)
- System dependencies installation
- Health checks
- Gunicorn WSGI server
- Static files collection

**Key Settings**:
- Port: 8000
- Workers: 4
- Worker class: sync
- Timeout: 120 seconds

**Build Command**:
```bash
docker build -t smartcart:latest .
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/Dockerfile`

---

### 4. **docker-compose.yml** ✅ CREATED
**Purpose**: Multi-container orchestration for local development
**Services**:
1. **db** - PostgreSQL 15
2. **redis** - Redis 7 (cache & message broker)
3. **web** - Django application
4. **celery** - Async task worker
5. **celery-beat** - Scheduled task runner
6. **flower** - Celery monitoring UI

**Volumes**:
- postgres_data: Database persistence
- redis_data: Redis persistence
- static_volume: Static files
- media_volume: User uploads

**Network**: smartcart_network (bridge)

**Start Services**:
```bash
docker-compose up -d
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/docker-compose.yml`

---

### 5. **pytest.ini** ✅ CREATED
**Purpose**: Pytest configuration for testing
**Configuration**:
- Django settings module
- Test file patterns
- Coverage reporting (HTML, terminal, XML)
- Custom markers (slow, integration, unit, celery, payment, auth)
- Test paths for each app

**Run Tests**:
```bash
pytest                 # All tests
pytest --cov=.        # With coverage
pytest -m integration # Specific marker
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/pytest.ini`

---

### 6. **.dockerignore** ✅ CREATED
**Purpose**: Specifies files to exclude when building Docker image
**Excludes**:
- Git files and directories
- Python cache and virtual environments
- Django temporary files
- IDE/Editor settings
- Testing coverage files
- Documentation and markdown
- Environment files
- Node modules and CI/CD files

**Reduces image size and build time**

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/.dockerignore`

---

### 7. **.coveragerc** ✅ CREATED
**Purpose**: Code coverage configuration
**Settings**:
- Branch coverage enabled
- Source code directories
- Omit patterns (tests, migrations, venv)
- Report settings (precision, missing lines)
- HTML report directory: htmlcov/
- XML report for CI/CD

**Generate Coverage Report**:
```bash
pytest --cov=. --cov-report=html
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/.coveragerc`

---

### 8. **Makefile** ✅ CREATED
**Purpose**: Convenient command shortcuts
**Categories**:
- Setup & Installation
- Development commands
- Docker operations
- Testing
- Code quality
- Celery
- Database operations
- Utilities

**Usage Examples**:
```bash
make help              # Show all commands
make install           # Install dependencies
make docker-up         # Start Docker services
make test              # Run tests
make format            # Format code
make celery            # Run Celery worker
```

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/Makefile`

---

### 9. **.editorconfig** ✅ CREATED
**Purpose**: Maintain consistent code styling across editors
**Settings**:
- Charset: UTF-8
- Line endings: LF
- Python: 4-space indentation
- JSON/YAML: 2-space indentation
- HTML/CSS: 2-space indentation
- Max line length: 100 characters

**Supported by**: VSCode, PyCharm, Sublime, Vim, etc.

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/.editorconfig`

---

### 10. **CONTRIBUTING.md** ✅ CREATED
**Purpose**: Guidelines for contributors
**Sections**:
- Code of Conduct
- Getting Started
- Development Workflow
- Code Style (PEP 8, Black, isort)
- Testing requirements
- Commit message conventions
- Pull Request process
- Areas for contribution
- Issue reporting templates

**Usage**: Reference for contributors

**Location**: `/Users/olajideojo/Desktop/alx-project-nexus/CONTRIBUTING.md`

---

## File Structure Summary

```
alx-project-nexus/
├── .gitignore                 # Git ignore patterns
├── .env.example               # Environment variables template
├── .dockerignore              # Docker build exclusions
├── .editorconfig              # Editor configuration
├── Dockerfile                 # Docker image specification
├── docker-compose.yml         # Multi-container orchestration
├── pytest.ini                 # Testing configuration
├── .coveragerc               # Code coverage configuration
├── Makefile                  # Command shortcuts
├── CONTRIBUTING.md           # Contributor guidelines
├── project-setup.md          # Project documentation
├── requirements.txt          # Python dependencies
└── ...                       # Other project files
```

---

## Environment Variables

### Required for Development
```bash
SECRET_KEY              # Django secret key
DATABASE_PASSWORD       # PostgreSQL password
```

### Required for Production
```bash
DEBUG=False
ALLOWED_HOSTS          # Domain names
SECRET_KEY             # Strong secret key
DATABASE_PASSWORD      # Secure password
PAYSTACK_SECRET_KEY    # Payment gateway key
EMAIL_HOST_PASSWORD    # Email service password
```

---

## Quick Commands Reference

```bash
# Development
make install && make runserver

# Docker
make docker-build && make docker-up

# Testing
make test-coverage

# Code Quality
make check

# Celery
make celery
make flower  # Visit http://localhost:5555

# Database
make migrate
make createsuperuser
```

---

## Configuration Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Update `.env` with actual values
- [ ] Install dependencies: `make install`
- [ ] Run migrations: `make migrate`
- [ ] Create superuser: `make createsuperuser`
- [ ] Run tests: `make test`
- [ ] Format code: `make format`

---

## References

- Django: https://docs.djangoproject.com/
- Docker: https://docs.docker.com/
- Pytest: https://docs.pytest.org/
- Black (Code Formatter): https://black.readthedocs.io/
- EditorConfig: https://editorconfig.org/

---

**Last Updated**: November 11, 2025
