# Capastan Sentiment Analysis

A production-ready sentiment analysis application that classifies text (e.g., reviews, social media posts, customer feedback) into positive, negative, or neutral categories. The project follows modern MLOps best practices and is designed for scalable deployment.

## Project Overview

This repository implements an end-to-end sentiment analysis pipeline using Python, with:

- Data ingestion and versioning using **DVC**
- Feature engineering and model training
- A lightweight **Flask** REST API for real-time predictions
- Containerization with **Docker**
- Kubernetes manifests for deployment

The project structure adheres to the [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) template.

## Key Features

- Reproducible data and ML pipelines with **DVC**
- Model training and inference scripts in `src/`
- Web service (`flask_app/`) exposing a `/predict` endpoint
- Containerized application ready for cloud orchestration
- Unit tests and tox configuration
- CI/CD hooks via GitHub Actions (extendable)

## Architecture & Technology Stack

- **Language & Frameworks**: Python, scikit-learn / transformers (configurable), Flask
- **Data & Pipeline Management**: DVC, pandas, numpy
- **Containerization**: Docker
- **Orchestration (recommended)**: Kubernetes on AWS EKS
- **Monitoring (recommended)**: Prometheus + Grafana
- **Documentation**: Sphinx (`docs/`)

## Why AWS EKS, Prometheus, and Grafana?

This project can be deployed locally or on any Kubernetes cluster. However, production usage benefits significantly from cloud-managed Kubernetes and observability tooling.

### AWS Elastic Kubernetes Service (EKS)

**Why EKS?**

- Fully managed Kubernetes control plane — eliminates the operational burden of managing etcd, API servers, and upgrades.
- Native integration with AWS services: IAM roles for pods (IRSA), VPC networking, ALB Ingress, ECR for images, CloudWatch for logs.
- High availability and auto-scaling across multiple availability zones.
- Cost-effective scaling for variable inference traffic (e.g., HPA + Cluster Autoscaler).
- Enterprise-grade security: private clusters, security groups, encryption at rest/transit.

**How it is used / recommended setup**

1. Build and push the Docker image to **Amazon ECR**.
2. Apply the provided `deployment.yaml` (and optional service/ingress manifests) to an EKS cluster.
3. Use `kubectl` or GitOps tools (ArgoCD / Flux) for deployment.
4. Expose the Flask app via an AWS Application Load Balancer (ALB Ingress Controller).
5. Scale pods automatically based on CPU/memory or custom metrics (e.g., requests per second).

### Prometheus & Grafana

**Why Prometheus and Grafana?**

- Prometheus provides robust, pull-based metrics collection — the de facto standard in Kubernetes ecosystems.
- Grafana delivers rich, customizable dashboards and alerting for both infrastructure and application metrics.
- Together they enable:
  - Monitoring pod health, CPU/memory usage, API latency, error rates
  - Custom business metrics (e.g., prediction throughput, average latency per sentiment class)
  - Early detection of model drift, service degradation, or resource exhaustion
  - Alerting via Slack/PagerDuty/email when thresholds are breached

**How they are integrated (recommended)**

1. Install the **Prometheus Operator** (or kube-prometheus-stack via Helm) on the EKS cluster.
2. Add annotations to the Deployment/Service:
   ```yaml
   metadata:
     annotations:
       prometheus.io/scrape: "true"
       prometheus.io/port: "5000"   # Flask metrics endpoint port

Instrument the Flask app with prometheus-flask-exporter (add to requirements.txt):Pythonfrom prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
Create a ServiceMonitor CRD to let Prometheus discover the app.
Import community or custom Grafana dashboards for:
Kubernetes cluster overview
Flask/HTTP request metrics (latency, 4xx/5xx rates)
Python runtime metrics (GC, threads)

Set up alerts for high error rates, latency > 500 ms, or low throughput.

Getting Started
Prerequisites

Python 3.8+
Docker
kubectl (for Kubernetes deployment)
AWS CLI + eksctl (for EKS)

Local Development
Bash# Clone repository
git clone https://github.com/shekhus/capastan_sentiment_analysis.git
cd capastan_sentiment_analysis

# Install dependencies
pip install -r requirements.txt

# Reproduce pipeline (data → features → model)
dvc repro

# Run Flask API locally
cd flask_app
python app.py
Test the endpoint:
Bashcurl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"text": "This product is excellent!"}'
Docker Build & Run
Bashdocker build -t capastan-sentiment:latest .
docker run -p 5000:5000 capastan-sentiment:latest
Deployment to AWS EKS (example)

Create/push image to ECR
Configure kubectl context to EKS cluster
Apply manifests:Bashkubectl apply -f deployment.yaml
kubectl apply -f service.yaml          # if present
kubectl apply -f ingress.yaml          # optional

Project Structure
See the Cookiecutter Data Science documentation for detailed folder explanations.
text├── data/               # Raw, interim, processed data
├── docs/               # Sphinx documentation
├── flask_app/          # Flask prediction service
├── models/             # Trained models
├── notebooks/          # Exploratory analysis
├── src/                # Core pipeline code
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── tests/
├── deployment.yaml     # Kubernetes deployment manifest
├── Dockerfile
├── dvc.yaml
└── requirements.txt
License
MIT License — see LICENSE for details.
Contributing
Contributions are welcome. Please open an issue first to discuss proposed changes.
