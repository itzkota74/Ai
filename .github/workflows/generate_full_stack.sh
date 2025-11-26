#!/bin/bash
set -euo pipefail

WORKDIR=$(pwd)
GODHEAD_DIR="$WORKDIR/godhead"

# Create directories
mkdir -p "$GODHEAD_DIR/manifests" "$GODHEAD_DIR/scripts" "$GODHEAD_DIR/api" "$GODHEAD_DIR/infra" "$GODHEAD_DIR/monitoring"

# Manifest template
MANIFEST_FILE="$GODHEAD_DIR/manifests/manifest.yaml"
cat <<MANIFEST > "$MANIFEST_FILE"
tasks:
  - name: train_model
    priority: 10
    auto: true
  - name: deploy_k8s
    priority: 8
    auto: true
  - name: update_dashboards
    priority: 5
    auto: true
MANIFEST

# Orchestrator
ORCH="$GODHEAD_DIR/orchestrator.py"
cat <<ORCH_PY > "$ORCH"
#!/usr/bin/env python3
import yaml, sys
manifest_path = sys.argv[1] if len(sys.argv) > 1 else "godhead/manifests/manifest.yaml"
with open(manifest_path) as f:
    manifest = yaml.safe_load(f)
print("[INFO] Running tasks in manifest...")
for task in manifest.get("tasks", []):
    if task.get("auto", False):
        print(f"[RUN] {task['name']}")
ORCH_PY

# API
mkdir -p "$GODHEAD_DIR/api"
cat <<API_PY > "$GODHEAD_DIR/api/model_api.py"
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class InputData(BaseModel):
    instances: list
@app.post("/predict")
def predict(data: InputData):
    return {"predictions": [[0.1, 0.9]]}
API_PY

# Dockerfile
cat <<DOCKER > "$GODHEAD_DIR/Dockerfile"
FROM python:3.12-slim
WORKDIR /app
COPY ./godhead ./godhead
COPY ./api ./api
RUN pip install --no-cache-dir fastapi uvicorn pyyaml requests mlflow
CMD ["uvicorn", "api.model_api:app", "--host", "0.0.0.0", "--port", "8080"]
DOCKER

# Docker Compose
cat <<DCOMPOSE > "$GODHEAD_DIR/docker-compose.yml"
version: "3.9"
services:
  godhead-api:
    build: .
    container_name: godhead-api
    ports:
      - "8080:8080"
    environment:
      - MLFLOW_TRACKING_URI=\${MLFLOW_TRACKING_URI}
      - MLFLOW_S3_ENDPOINT_URL=\${MLFLOW_S3_ENDPOINT_URL}
DCOMPOSE

# Scripts
mkdir -p "$GODHEAD_DIR/scripts"
cat <<BOOTSTRAP > "$GODHEAD_DIR/scripts/bootstrap_ci.sh"
#!/bin/bash
set -euo pipefail
echo "[INFO] CI/CD Bootstrap..."
docker build -t ghcr.io/your-org/godhead:latest .
docker push ghcr.io/your-org/godhead:latest
terraform init && terraform plan
BOOTSTRAP

chmod -R 755 "$GODHEAD_DIR/scripts" "$GODHEAD_DIR/api" "$ORCH"
echo "[DONE] Full Godhead stack created!"
