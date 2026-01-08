# 🛒 SmartCart E-Commerce — ALX Capstone Project

---

## 📜 License References

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen)
![DRF](https://img.shields.io/badge/DRF-REST--Framework-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![Paystack](https://img.shields.io/badge/Paystack-Payments-1099BB)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)


> **A full-featured, secure, and scalable e-commerce backend built with Django, PostgreSQL, Celery, Redis, and Docker.**  
> Designed and developed as part of the **ALX ProDev Backend Engineering Capstone**.

---

## 🚀 Overview

SmartCart is a modular e-commerce platform built to simulate a real-world system.  
It supports user authentication, product management, cart operations, order processing, payment tracking, and asynchronous notifications — all following **industry best practices**.

This project demonstrates backend architecture skills including:
- **Database modeling**
- **API design**
- **Celery for background tasks**
- **Containerization (Docker)**
- **Continuous Integration and Deployment readiness**

---

## 🧠 Features

✅ User authentication with JWT  
✅ Product listing and category management  
✅ Shopping cart and checkout workflow  
✅ Order creation and tracking  
✅ Payment processing logic  
✅ Email and notification system (Celery + Redis)  
✅ Admin dashboard for managing products and orders  
✅ RESTful API architecture using Django REST Framework  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend Framework** | Django 5 + Django REST Framework |
| **Database** | PostgreSQL |
| **Caching & Queues** | Redis + Celery |
| **Containerization** | Docker + Docker Compose |
| **Auth System** | JWT (via `djangorestframework-simplejwt`) |
| **Documentation** | Swagger / DRF-Yasg |
| **Testing** | Pytest + Django Test Framework |
| **Deployment Ready For** | Kubernetes + Nginx Ingress |

---

## 📁 Project Folder Structure

```
alx-project-nexus/
├── SwiftCart/                          # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py                         # ASGI configuration for async support
│   ├── wsgi.py                         # WSGI configuration for production servers
│   ├── settings.py                     # Django settings (database, apps, middleware, etc.)
│   ├── urls.py                         # Main URL router
│   └── celery.py                       # Celery configuration (async tasks)
│
├── authentication/                     # User authentication & authorization
│   ├── __init__.py
│   ├── admin.py                        # Django admin customization
│   ├── apps.py                         # App configuration
│   ├── models.py                       # User model and related auth models
│   ├── serializers.py                  # DRF serializers for auth endpoints
│   ├── tests.py                        # Unit tests for authentication
│   ├── urls.py                         # Auth-related URL routes
│   ├── views.py                        # JWT login, signup, token refresh
│   └── migrations/                     # Database migration files
│       └── __init__.py
│
├── products/                           # Product management & catalog
│   ├── __init__.py
│   ├── admin.py                        # Admin interface for products
│   ├── apps.py                         # App configuration
│   ├── models.py                       # Product, Category, Review models
│   ├── serializers.py                  # Product serializers
│   ├── tests.py                        # Product tests
│   ├── urls.py                         # Product endpoints (/products/, /categories/)
│   ├── views.py                        # Product listing, filtering, search
│   └── migrations/
│       └── __init__.py
│
├── cart/                               # Shopping cart operations
│   ├── __init__.py
│   ├── admin.py                        # Cart admin
│   ├── apps.py                         # App configuration
│   ├── models.py                       # Cart, CartItem models
│   ├── serializers.py                  # Cart serializers
│   ├── tests.py                        # Cart tests
│   ├── urls.py                         # Cart routes (/cart/)
│   ├── views.py                        # Add to cart, remove, update quantities
│   └── migrations/
│       └── __init__.py
│
├── orders/                             # Order processing & management
│   ├── __init__.py
│   ├── admin.py                        # Order admin interface
│   ├── apps.py                         # App configuration
│   ├── models.py                       # Order, OrderItem, OrderStatus models
│   ├── serializers.py                  # Order serializers
│   ├── tests.py                        # Order tests
│   ├── urls.py                         # Order endpoints (/orders/)
│   ├── views.py                        # Create order, list orders, order details
│   └── migrations/
│       └── __init__.py
│
├── payments/                           # Payment processing (Paystack integration)
│   ├── __init__.py
│   ├── admin.py                        # Payment admin
│   ├── apps.py                         # App configuration
│   ├── models.py                       # Payment, Transaction models
│   ├── paystack_service.py             # Paystack API integration logic
│   ├── serializers.py                  # Payment serializers
│   ├── tests.py                        # Payment tests
│   ├── views.py                        # Payment initiation, verification
│   └── migrations/
│       └── __init__.py
│
├── notifications/                      # Email & notification system
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py                         # App configuration
│   ├── models.py                       # Notification, Email models
│   ├── tests.py                        # Notification tests
│   ├── views.py                        # Notification endpoints
│   ├── tasks.py                        # Celery tasks for async emails
│   └── migrations/
│       └── __init__.py
│
├── manage.py                           # Django management command entry point
├── setup_apps.py                       # Script to initialize installed apps
├── requirements.txt                    # Python dependencies & versions
├── README.md                           # Project overview & quick start
├── project-setup.md                    # Detailed setup & deployment guide (this file)
├── LICENSE                             # MIT License with third-party references
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Example environment variables template
├── docker-compose.yml                  # Docker Compose for local development
├── Dockerfile                          # Docker image configuration
├── pytest.ini                          # Pytest configuration
├── k8s/                                # Kubernetes deployment manifests
│   ├── namespace.yaml                  # K8s namespace definition
│   ├── configmap.yaml                  # Environment configuration
│   ├── secret.yaml                     # Secrets (API keys, passwords)
│   ├── postgres.yaml                   # PostgreSQL deployment
│   ├── redis.yaml                      # Redis deployment
│   ├── web.yaml                        # Django web service
│   ├── celery-worker.yaml              # Celery worker deployment
│   ├── celery-beat.yaml                # Celery scheduler deployment
│   └── ingress.yaml                    # Nginx ingress controller
│
└── static/                             # Static files (CSS, JS, images)
    └── admin/                          # Django admin static files
```

### 🔑 Key Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| **SwiftCart** | Core Django project settings and configuration |
| **authentication** | User login, registration, JWT token management |
| **products** | Product catalog, categories, search, filtering |
| **cart** | Shopping cart logic, item management |
| **orders** | Order creation, tracking, status management |
| **payments** | Payment processing via Paystack |
| **notifications** | Email notifications and async task handling via Celery |
| **k8s** | Kubernetes YAML manifests for cloud deployment |

---

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **POST** | `/api/auth/register/` | User registration | No |
| **POST** | `/api/auth/login/` | User login (returns JWT tokens) | No |
| **POST** | `/api/auth/token/refresh/` | Refresh access token | No |
| **POST** | `/api/auth/logout/` | User logout | Yes |
| **GET** | `/api/auth/profile/` | Get current user profile | Yes |
| **PUT** | `/api/auth/profile/update/` | Update user profile | Yes |
| **POST** | `/api/auth/password-change/` | Change user password | Yes |
| **POST** | `/api/auth/password-reset/` | Request password reset | No |
| **POST** | `/api/auth/password-reset-confirm/` | Confirm password reset | No |

**Sample Login Request:**
```json
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Sample Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **GET** | `/api/products/` | List all products with pagination & filtering | No |
| **POST** | `/api/products/` | Create new product (Admin only) | Yes |
| **GET** | `/api/products/<id>/` | Get product details | No |
| **PUT** | `/api/products/<id>/` | Update product (Admin only) | Yes |
| **DELETE** | `/api/products/<id>/` | Delete product (Admin only) | Yes |
| **GET** | `/api/products/<id>/reviews/` | Get product reviews | No |
| **POST** | `/api/products/<id>/reviews/` | Add product review | Yes |
| **GET** | `/api/categories/` | List all product categories | No |
| **POST** | `/api/categories/` | Create category (Admin only) | Yes |
| **GET** | `/api/categories/<id>/` | Get category details | No |
| **GET** | `/api/products/search/` | Search products by name/description | No |

**Sample Product Listing Request:**
```http
GET /api/products/?page=1&limit=10&category=electronics&min_price=100&max_price=5000&search=laptop
```

**Sample Product Response:**
```json
{
  "count": 25,
  "next": "/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Laptop Pro",
      "description": "High-performance laptop",
      "price": "1999.99",
      "category": "electronics",
      "stock": 50,
      "rating": 4.5,
      "image_url": "https://..."
    }
  ]
}
```

---

### Shopping Cart Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **GET** | `/api/cart/` | Get user's shopping cart | Yes |
| **POST** | `/api/cart/items/` | Add item to cart | Yes |
| **PUT** | `/api/cart/items/<id>/` | Update cart item quantity | Yes |
| **DELETE** | `/api/cart/items/<id>/` | Remove item from cart | Yes |
| **DELETE** | `/api/cart/clear/` | Clear entire cart | Yes |
| **GET** | `/api/cart/summary/` | Get cart summary (total, item count) | Yes |

**Sample Add to Cart Request:**
```json
POST /api/cart/items/
{
  "product_id": 1,
  "quantity": 2
}
```

**Sample Cart Response:**
```json
{
  "id": "cart-uuid",
  "user_id": 1,
  "items": [
    {
      "id": "cart-item-id",
      "product": {
        "id": 1,
        "name": "Laptop Pro",
        "price": "1999.99"
      },
      "quantity": 2,
      "subtotal": "3999.98"
    }
  ],
  "total_items": 2,
  "total_price": "3999.98",
  "updated_at": "2025-11-11T10:30:00Z"
}
```

---

### Order Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **POST** | `/api/orders/` | Create new order from cart | Yes |
| **GET** | `/api/orders/` | List user's orders | Yes |
| **GET** | `/api/orders/<id>/` | Get order details | Yes |
| **PUT** | `/api/orders/<id>/` | Update order status (Admin only) | Yes |
| **DELETE** | `/api/orders/<id>/` | Cancel order (if pending) | Yes |
| **GET** | `/api/orders/<id>/invoice/` | Download order invoice | Yes |
| **POST** | `/api/orders/<id>/track/` | Track order shipment | Yes |

**Sample Create Order Request:**
```json
POST /api/orders/
{
  "shipping_address": {
    "street": "123 Main St",
    "city": "Lagos",
    "state": "Lagos",
    "postal_code": "100001",
    "country": "Nigeria"
  },
  "payment_method": "card",
  "notes": "Please handle with care"
}
```

**Sample Order Response:**
```json
{
  "id": "ORD-2025-001",
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": "1999.99",
      "subtotal": "3999.98"
    }
  ],
  "subtotal": "3999.98",
  "shipping_cost": "500.00",
  "tax": "640.00",
  "total": "5139.98",
  "status": "pending",
  "shipping_address": {...},
  "created_at": "2025-11-11T10:30:00Z",
  "estimated_delivery": "2025-11-15"
}
```

---

### Payment Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **POST** | `/api/payments/initialize/` | Initialize payment with Paystack | Yes |
| **GET** | `/api/payments/verify/<reference>/` | Verify payment status | Yes |
| **GET** | `/api/payments/` | List user payment history | Yes |
| **GET** | `/api/payments/<id>/` | Get payment details | Yes |
| **POST** | `/api/payments/webhook/` | Paystack webhook callback | No |

**Sample Initialize Payment Request:**
```json
POST /api/payments/initialize/
{
  "order_id": "ORD-2025-001",
  "amount": 5139.98,
  "email": "user@example.com"
}
```

**Sample Payment Response:**
```json
{
  "id": "PAY-001",
  "order_id": "ORD-2025-001",
  "amount": 5139.98,
  "currency": "NGN",
  "status": "pending",
  "payment_url": "https://checkout.paystack.com/...",
  "reference": "ref_1234567890",
  "created_at": "2025-11-11T10:30:00Z"
}
```

---

### Notification Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **GET** | `/api/notifications/` | Get user notifications | Yes |
| **GET** | `/api/notifications/<id>/` | Get notification details | Yes |
| **PUT** | `/api/notifications/<id>/read/` | Mark notification as read | Yes |
| **DELETE** | `/api/notifications/<id>/` | Delete notification | Yes |
| **PUT** | `/api/notifications/read-all/` | Mark all as read | Yes |
| **GET** | `/api/notifications/preferences/` | Get notification preferences | Yes |
| **PUT** | `/api/notifications/preferences/` | Update notification preferences | Yes |

**Sample Notification Response:**
```json
{
  "id": "notif-001",
  "user_id": 1,
  "type": "order_status",
  "title": "Order Confirmed",
  "message": "Your order ORD-2025-001 has been confirmed",
  "is_read": false,
  "created_at": "2025-11-11T10:30:00Z"
}
```

---

### Admin Endpoints (Staff Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| **GET** | `/api/admin/dashboard/` | Dashboard statistics | Yes (Staff) |
| **GET** | `/api/admin/users/` | List all users | Yes (Staff) |
| **GET** | `/api/admin/orders/` | List all orders | Yes (Staff) |
| **GET** | `/api/admin/reports/sales/` | Sales reports | Yes (Staff) |
| **GET** | `/api/admin/reports/revenue/` | Revenue reports | Yes (Staff) |
| **POST** | `/api/admin/products/bulk-upload/` | Bulk product upload | Yes (Staff) |

---

## 🛡️ Authentication & Authorization

### JWT Token Headers
All authenticated requests require the JWT token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Token Expiry
- **Access Token**: 15 minutes
- **Refresh Token**: 7 days

### Refresh Token Flow
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 📊 Response Format

All API responses follow this standard format:

### Success Response (2xx)
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response (4xx, 5xx)
```json
{
  "status": "error",
  "error_code": "INVALID_REQUEST",
  "message": "Detailed error message",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

---

## 🧪 Testing API Endpoints

### Using cURL
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'

# Get products
curl -X GET http://localhost:8000/api/products/ \
  -H "Content-Type: application/json"
```

### Using Postman
1. Import the API collection (to be added)
2. Set environment variables for `BASE_URL` and `JWT_TOKEN`
3. Run requests from the collection

### Using Swagger UI
- Access interactive API documentation at: `http://localhost:8000/swagger/`
- Test endpoints directly from the browser

---

## 🐳 Docker Setup (for Local Development)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Quick Start with Docker

1. **Clone the repository:**
```bash
git clone https://github.com/<your-username>/alx-project-nexus.git
cd alx-project-nexus
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Build and start all services:**
```bash
docker-compose up -d
```

This command will start:
- **web**: Django application on `http://localhost:8000`
- **db**: PostgreSQL database on `localhost:5432`
- **redis**: Redis cache on `localhost:6379`
- **celery**: Celery worker for async tasks
- **celery-beat**: Celery scheduler for periodic tasks

4. **Run database migrations:**
```bash
docker-compose exec web python manage.py migrate
```

5. **Create a superuser account:**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Load sample data (optional):**
```bash
docker-compose exec web python manage.py loaddata initial_data
```

### Accessing the Application

| Service | URL |
|---------|-----|
| **API** | http://localhost:8000 |
| **Swagger Docs** | http://localhost:8000/swagger/ |
| **Admin Panel** | http://localhost:8000/admin/ |
| **Flower (Celery Monitor)** | http://localhost:5555 |

### Useful Docker Compose Commands

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db
```

**Stop services:**
```bash
docker-compose down
```

**Stop and remove all data:**
```bash
docker-compose down -v
```

**Rebuild images:**
```bash
docker-compose build --no-cache
```

**Run management commands:**
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Run tests
docker-compose exec web python manage.py test

# Django shell
docker-compose exec web python manage.py shell
```

**Access container shell:**
```bash
# Django container
docker-compose exec web bash

# Database container
docker-compose exec db psql -U postgres -d smartcart_db

# Redis container
docker-compose exec redis redis-cli
```

### Docker Compose Services Explained

**web** - Django application container
- Port: 8000
- Depends on: db, redis
- Environment: Loaded from `.env` file

**db** - PostgreSQL database container
- Port: 5432
- Volume: Persistent data storage (`postgres_data`)
- Default database: `smartcart_db`

**redis** - Redis cache and message broker
- Port: 6379
- Used by: Celery for task queue

**celery** - Celery worker for async tasks
- Processes background jobs
- Connects to: Redis and PostgreSQL

**celery-beat** - Celery beat scheduler
- Runs periodic/scheduled tasks
- Interval-based task scheduling

### Dockerfile Overview

The `Dockerfile` includes:
- **Base Image**: Python 3.10 slim
- **Dependencies**: Installed from `requirements.txt`
- **Static Files**: Collected during build
- **Working Directory**: `/app`
- **Exposed Port**: 8000

### docker-compose.yml Overview

The compose file defines:
- Service configurations
- Network settings (default bridge network)
- Volume mounts for data persistence
- Environment variables
- Health checks
- Dependencies between services

### Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Maps host port 8001 to container port 8000
```

**Permission denied errors:**
```bash
# On Linux, you may need to use sudo
sudo docker-compose up -d
```

**Database connection errors:**
```bash
# Ensure db service is running
docker-compose ps

# Check logs
docker-compose logs db
```

**Clear all containers and volumes:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## ☸️ Kubernetes Deployment

Kubernetes provides production-grade container orchestration, auto-scaling, and self-healing capabilities.

### Prerequisites

- [kubectl](https://kubernetes.io/docs/tasks/tools/) (v1.24+)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local testing) OR access to a cloud cluster:
  - AWS EKS
  - Google Cloud GKE
  - Azure AKS
  - DigitalOcean Kubernetes

### Quick Start with Minikube (Local Testing)

**1. Start Minikube:**
```bash
minikube start --cpus=4 --memory=8192 --disk-size=50g
```

**2. Enable Ingress addon:**
```bash
minikube addons enable ingress
```

**3. Create namespace:**
```bash
kubectl create namespace smartcart
```

**4. Apply configurations:**
```bash
# Create secrets
kubectl apply -f k8s/secret.yaml -n smartcart

# Create ConfigMap
kubectl apply -f k8s/configmap.yaml -n smartcart

# Deploy database and cache
kubectl apply -f k8s/postgres.yaml -n smartcart
kubectl apply -f k8s/redis.yaml -n smartcart

# Wait for db and redis to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n smartcart --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n smartcart --timeout=300s

# Deploy application
kubectl apply -f k8s/web.yaml -n smartcart
kubectl apply -f k8s/celery-worker.yaml -n smartcart
kubectl apply -f k8s/celery-beat.yaml -n smartcart

# Apply Ingress
kubectl apply -f k8s/ingress.yaml -n smartcart
```

**5. Access the application:**
```bash
# Get the Minikube IP
minikube ip

# Access the application (replace <minikube-ip> with actual IP)
http://<minikube-ip>
```

### Kubernetes Manifest Files

#### **1. Namespace (`k8s/namespace.yaml`)**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: smartcart
  labels:
    environment: production
```

#### **2. ConfigMap (`k8s/configmap.yaml`)**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: smartcart-config
  namespace: smartcart
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "smartcart.example.com,localhost"
  CELERY_BROKER_URL: "redis://redis-service:6379/0"
  CELERY_RESULT_BACKEND: "redis://redis-service:6379/0"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "smartcart_db"
  ENVIRONMENT: "production"
```

#### **3. Secret (`k8s/secret.yaml`)**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: smartcart-secret
  namespace: smartcart
type: Opaque
stringData:
  SECRET_KEY: "your-secret-key-here-change-in-production"
  DB_PASSWORD: "secure-postgres-password"
  DB_USER: "postgres"
  PAYSTACK_KEY: "your-paystack-key"
  PAYSTACK_SECRET: "your-paystack-secret"
```

#### **4. PostgreSQL Deployment (`k8s/postgres.yaml`)**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: smartcart
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: smartcart
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: smartcart
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: DATABASE_NAME
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: DB_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: DB_PASSWORD
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          subPath: postgres
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

#### **5. Redis Deployment (`k8s/redis.yaml`)**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: smartcart
spec:
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: smartcart
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
```

#### **6. Django Web Service (`k8s/web.yaml`)**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: smartcart
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: smartcart
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: smartcart:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: DEBUG
        - name: ALLOWED_HOSTS
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: ALLOWED_HOSTS
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: SECRET_KEY
        - name: DATABASE_URL
          value: "postgresql://postgres:$(DB_PASSWORD)@postgres-service:5432/smartcart_db"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: DB_PASSWORD
        - name: CELERY_BROKER_URL
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: CELERY_BROKER_URL
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
```

#### **7. Celery Worker (`k8s/celery-worker.yaml`)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-worker
  namespace: smartcart
spec:
  replicas: 2
  selector:
    matchLabels:
      app: celery-worker
  template:
    metadata:
      labels:
        app: celery-worker
    spec:
      containers:
      - name: celery-worker
        image: smartcart:latest
        imagePullPolicy: Always
        command: ["celery", "-A", "SwiftCart", "worker", "-l", "info"]
        env:
        - name: CELERY_BROKER_URL
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: CELERY_BROKER_URL
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: SECRET_KEY
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
```

#### **8. Celery Beat (`k8s/celery-beat.yaml`)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-beat
  namespace: smartcart
spec:
  replicas: 1
  selector:
    matchLabels:
      app: celery-beat
  template:
    metadata:
      labels:
        app: celery-beat
    spec:
      containers:
      - name: celery-beat
        image: smartcart:latest
        imagePullPolicy: Always
        command: ["celery", "-A", "SwiftCart", "beat", "-l", "info"]
        env:
        - name: CELERY_BROKER_URL
          valueFrom:
            configMapKeyRef:
              name: smartcart-config
              key: CELERY_BROKER_URL
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: smartcart-secret
              key: SECRET_KEY
        resources:
          limits:
            memory: "256Mi"
            cpu: "250m"
          requests:
            memory: "128Mi"
            cpu: "100m"
```

---

## 🌐 Nginx Ingress Configuration

Ingress manages external access to services and provides load balancing, SSL termination, and routing.

### Prerequisites

**Install Nginx Ingress Controller:**

**For Minikube:**
```bash
minikube addons enable ingress
```

**For cloud clusters (AWS EKS, GCP GKE, etc.):**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

**For Azure AKS:**
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
```

### Ingress Configuration (`k8s/ingress.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: smartcart-ingress
  namespace: smartcart
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - smartcart.example.com
    secretName: smartcart-tls
  rules:
  - host: smartcart.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /api/
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /admin/
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /swagger/
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Useful Ingress Commands

**Check Ingress status:**
```bash
kubectl get ingress -n smartcart
kubectl describe ingress smartcart-ingress -n smartcart
```

**Get Ingress IP/hostname:**
```bash
kubectl get ingress smartcart-ingress -n smartcart -o wide
```

**Update DNS records:**
After getting the Ingress IP, update your DNS provider:
```
smartcart.example.com  A  <INGRESS-IP>
```

**Test Ingress:**
```bash
# Using curl with host header
curl -H "Host: smartcart.example.com" http://<INGRESS-IP>

# Or add to /etc/hosts (on Linux/Mac)
echo "<INGRESS-IP> smartcart.example.com" | sudo tee -a /etc/hosts
curl http://smartcart.example.com
```

---

### Kubernetes Management Commands

**View resources:**
```bash
# All resources
kubectl get all -n smartcart

# Specific resource types
kubectl get pods -n smartcart
kubectl get svc -n smartcart
kubectl get deploy -n smartcart
kubectl get ingress -n smartcart
```

**Describe resources:**
```bash
kubectl describe pod <pod-name> -n smartcart
kubectl describe svc web-service -n smartcart
kubectl describe ingress smartcart-ingress -n smartcart
```

**View logs:**
```bash
# Single pod
kubectl logs <pod-name> -n smartcart

# Follow logs
kubectl logs -f <pod-name> -n smartcart

# Last 100 lines
kubectl logs --tail=100 <pod-name> -n smartcart
```

**Execute commands in pod:**
```bash
# Interactive shell
kubectl exec -it <pod-name> -n smartcart -- bash

# Run command
kubectl exec <pod-name> -n smartcart -- python manage.py migrate
```

**Scale deployments:**
```bash
# Scale web deployment
kubectl scale deployment web --replicas=5 -n smartcart

# Scale celery workers
kubectl scale deployment celery-worker --replicas=4 -n smartcart
```

**Update deployment:**
```bash
# Update image
kubectl set image deployment/web web=smartcart:v2 -n smartcart

# Rollout status
kubectl rollout status deployment/web -n smartcart

# Rollback if needed
kubectl rollout undo deployment/web -n smartcart
```

**Delete resources:**
```bash
# Delete entire namespace
kubectl delete namespace smartcart

# Delete specific resource
kubectl delete deployment web -n smartcart
kubectl delete service web-service -n smartcart
```

**Apply changes:**
```bash
# Apply all YAML files
kubectl apply -f k8s/ -n smartcart

# Apply single file
kubectl apply -f k8s/web.yaml -n smartcart
```

---

## ⚙️ Local Setup Instructions (Without Docker)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/alx-project-nexus.git
cd alx-project-nexus

# Set up virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  

# or 
env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migration
python manage.py migrate

# Start the server
python manage.py runserver
```

### Access Swagger docs at

```http://127.0.0.1:8000/swagger/```


