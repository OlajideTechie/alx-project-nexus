# Kubernetes Deployment Guide for SmartCart

This directory contains Kubernetes manifests for deploying SmartCart in production.

## 📋 File Descriptions

### Deployment Order
Files are numbered to indicate the recommended deployment order:

| # | File | Description |
|---|------|-------------|
| 00 | `00-namespace.yaml` | Kubernetes namespace for resource isolation |
| 01 | `01-configmap.yaml` | Configuration variables |
| 02 | `02-secret.yaml` | Sensitive data (passwords, API keys) |
| 03 | `03-postgres.yaml` | PostgreSQL StatefulSet with persistent storage |
| 04 | `04-redis.yaml` | Redis deployment for caching & message broker |
| 05 | `05-web.yaml` | Django web application deployment |
| 06 | `06-celery-worker.yaml` | Celery worker deployment for async tasks |
| 07 | `07-celery-beat.yaml` | Celery beat scheduler deployment |
| 08 | `08-ingress.yaml` | Ingress, NetworkPolicy, and PodDisruptionBudgets |
| 09 | `09-autoscaling.yaml` | HPA, ResourceQuota, and LimitRange |
| 10 | `10-rbac.yaml` | Role-based access control |

## 🚀 Quick Start

### Prerequisites
```bash
# Install kubectl
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl

# Install Helm (optional, for Ingress Controller)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Setup kubeconfig for your cluster
kubectl config use-context <your-cluster-context>
```

### 1. Update Secrets
Edit `02-secret.yaml` with your actual values:
```bash
# Update these fields:
# - SECRET_KEY: Django secret key
# - DATABASE_PASSWORD: PostgreSQL password
# - EMAIL_HOST_PASSWORD: Email service password
# - PAYSTACK_PUBLIC_KEY & PAYSTACK_SECRET_KEY: Payment gateway keys
```

### 2. Update ConfigMap
Edit `01-configmap.yaml`:
```bash
# Update:
# - ALLOWED_HOSTS: Your domain names
# - DATABASE_NAME, DATABASE_USER: Database settings
# - EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER: Email settings
```

### 3. Install Ingress Controller (if not already installed)
```bash
# For AWS EKS
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/aws/deploy.yaml

# For GCP GKE
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# For Minikube
minikube addons enable ingress
```

### 4. Deploy All Resources
```bash
# Deploy in order (recommended)
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-configmap.yaml
kubectl apply -f 02-secret.yaml
kubectl apply -f 03-postgres.yaml
kubectl apply -f 04-redis.yaml

# Wait for database and cache to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n smartcart --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n smartcart --timeout=300s

# Deploy application
kubectl apply -f 05-web.yaml
kubectl apply -f 06-celery-worker.yaml
kubectl apply -f 07-celery-beat.yaml
kubectl apply -f 08-ingress.yaml
kubectl apply -f 09-autoscaling.yaml
kubectl apply -f 10-rbac.yaml

# Or deploy all at once:
kubectl apply -f k8s/
```

### 5. Verify Deployment
```bash
# Check all resources
kubectl get all -n smartcart

# Check pods status
kubectl get pods -n smartcart -w

# Check services
kubectl get svc -n smartcart

# Check ingress
kubectl get ingress -n smartcart

# View ingress details
kubectl describe ingress smartcart-ingress -n smartcart
```

## 📊 Resource Details

### StatefulSet
- **PostgreSQL** (03-postgres.yaml)
  - 1 replica with persistent storage (20Gi)
  - Health checks (liveness & readiness)
  - Resource requests: 256Mi memory, 250m CPU
  - Resource limits: 512Mi memory, 500m CPU

### Deployments
- **Web** (05-web.yaml): 3 replicas
  - Automatic migrations on startup
  - Health checks every 10 seconds
  - Rolling updates with 1 surge, 1 unavailable

- **Celery Worker** (06-celery-worker.yaml): 2 replicas
  - 4 concurrent tasks per worker
  - Max 1000 tasks per child process
  - 1-hour task time limit

- **Celery Beat** (07-celery-beat.yaml): 1 replica
  - Database-backed scheduler
  - Minimal resource usage

- **Redis** (04-redis.yaml): 1 replica
  - Appendonly persistence enabled
  - LRU eviction policy
  - Max memory: 256Mi

## 🔐 Security Features

### Implemented
- ✅ Non-root user containers (UID 1000)
- ✅ Read-only root filesystem (where applicable)
- ✅ Capability dropping
- ✅ Network policies for namespace isolation
- ✅ Resource quotas and limits
- ✅ RBAC with minimal permissions
- ✅ Secret management for sensitive data
- ✅ Security context per pod

### Recommended Additional Steps
1. Use Sealed Secrets or Vault for secret management
2. Enable RBAC at cluster level
3. Configure Pod Security Policies
4. Use network policies to restrict traffic
5. Enable audit logging
6. Configure image scanning

## 📈 Auto-Scaling

### Web Application HPA
- Minimum: 3 replicas
- Maximum: 10 replicas
- CPU threshold: 70% utilization
- Memory threshold: 80% utilization

### Celery Workers HPA
- Minimum: 2 replicas
- Maximum: 8 replicas
- CPU threshold: 75% utilization
- Memory threshold: 85% utilization

## 🔄 High Availability Features

### Pod Disruption Budgets
- Web: Minimum 2 available (minAvailable: 2)
- Celery Workers: Minimum 1 available (minAvailable: 1)

### Anti-Affinity
- Pods spread across different nodes
- Preferred pod affinity to nearby services

### Health Checks
- Liveness probes: Restarts unhealthy pods
- Readiness probes: Removes pods from traffic

## 💾 Data Persistence

### PostgreSQL
- StatefulSet with VolumeClaimTemplate
- 20Gi persistent storage
- Automatic backup recommended

### Redis
- In-memory with AOF persistence
- emptyDir volume (recreated on restart)
- Configure persistent volume if needed

## 🌐 Ingress Configuration

### Features
- TLS/SSL termination (Let's Encrypt)
- Rate limiting (100 req/min per IP)
- CORS support
- Security headers (X-Frame-Options, CSP)
- ModSecurity OWASP rules enabled

### Update Domain
1. Edit `08-ingress.yaml`
2. Replace `smartcart.example.com` with your domain
3. Update DNS records to point to Ingress IP

```bash
# Get Ingress IP
kubectl get ingress smartcart-ingress -n smartcart -o wide

# Add DNS record
# smartcart.example.com A <INGRESS_IP>
```

## 📝 Managing Deployments

### View Logs
```bash
# Web application
kubectl logs -f deployment/web -n smartcart

# Celery workers
kubectl logs -f deployment/celery-worker -n smartcart

# Celery beat
kubectl logs -f deployment/celery-beat -n smartcart

# PostgreSQL
kubectl logs -f statefulset/postgres -n smartcart

# Last 100 lines
kubectl logs --tail=100 -f deployment/web -n smartcart
```

### Scale Deployments
```bash
# Scale web
kubectl scale deployment web --replicas=5 -n smartcart

# Scale celery workers
kubectl scale deployment celery-worker --replicas=4 -n smartcart

# View replicas
kubectl get deployment -n smartcart
```

### Update Image
```bash
# Update web image
kubectl set image deployment/web web=smartcart:v2.0 -n smartcart

# Check rollout status
kubectl rollout status deployment/web -n smartcart

# Rollback if needed
kubectl rollout undo deployment/web -n smartcart
```

### Execute Commands
```bash
# Access pod shell
kubectl exec -it <pod-name> -n smartcart -- bash

# Run migrations
kubectl exec <web-pod> -n smartcart -- python manage.py migrate

# Create superuser
kubectl exec -it <web-pod> -n smartcart -- python manage.py createsuperuser

# Django shell
kubectl exec -it <web-pod> -n smartcart -- python manage.py shell
```

## 🛠️ Troubleshooting

### Pod Not Starting
```bash
# Check pod details
kubectl describe pod <pod-name> -n smartcart

# Check logs
kubectl logs <pod-name> -n smartcart

# Check events
kubectl get events -n smartcart
```

### Persistent Volume Issues
```bash
# Check PVC status
kubectl get pvc -n smartcart

# Describe PVC
kubectl describe pvc postgres-pvc -n smartcart

# Check storage class
kubectl get storageclass
```

### Database Connection Issues
```bash
# Test database connection
kubectl exec <web-pod> -n smartcart -- python manage.py dbshell

# Check database logs
kubectl logs -f statefulset/postgres -n smartcart
```

### Memory Issues
```bash
# Check resource usage
kubectl top pod -n smartcart

# Check resource quotas
kubectl describe resourcequota smartcart-quota -n smartcart
```

## 📊 Monitoring

### Prometheus Metrics
Pods expose metrics on port 8000 (`/metrics/` endpoint):
```bash
# Add ServiceMonitor for Prometheus operator
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: smartcart-monitor
  namespace: smartcart
spec:
  selector:
    matchLabels:
      app: web
  endpoints:
  - port: http
    interval: 30s
    path: /metrics/
EOF
```

### Logs
- Container logs: `kubectl logs`
- Centralized logging: Configure ELK, Loki, or Datadog
- Audit logs: Enable at cluster level

## 🔄 Backup & Recovery

### Database Backup
```bash
# Create backup
kubectl exec postgres-0 -n smartcart -- pg_dump -U postgres smartcart_db | gzip > backup.sql.gz

# Restore backup
zcat backup.sql.gz | kubectl exec -i postgres-0 -n smartcart -- psql -U postgres -d smartcart_db
```

### PVC Backup
```bash
# Using Velero
velero backup create smartcart-backup --include-namespaces smartcart
```

## 🗑️ Cleanup

### Delete Entire Deployment
```bash
kubectl delete namespace smartcart
```

### Delete Specific Resources
```bash
kubectl delete deployment web -n smartcart
kubectl delete statefulset postgres -n smartcart
kubectl delete pvc postgres-pvc -n smartcart
```

## 📚 References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Cert Manager](https://cert-manager.io/)
- [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

---

**Last Updated**: November 11, 2025
