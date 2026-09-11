# Aetheria Vertical AI Platform — Infrastructure + Deployment

Production-grade infrastructure for the Aetheria Vertical AI Knowledge Graph platform.

## Architecture

```
aetheria-vert/
├── .github/workflows/          # CI/CD pipelines
├── deploy/
│   ├── kubernetes/             # K8s manifests
│   │   ├── staging/
│   │   └── production/
│   └── terraform/              # Infrastructure as Code
├── monitoring/
│   ├── grafana/dashboards/     # Grafana dashboards
│   └── prometheus/             # Prometheus config
├── benchmark/                  # Performance benchmarking
├── scripts/                    # Deployment scripts
└── docker-compose.yml          # Full platform orchestration
```

## Quick Start

```bash
# Local development
docker-compose up -d

# Deploy to staging
kubectl apply -f deploy/kubernetes/staging/

# Deploy to production
kubectl apply -f deploy/kubernetes/production/

# Provision infrastructure
cd deploy/terraform/
terraform init
terraform apply
```
