FROM python:3.12-slim
WORKDIR /app
COPY ./godhead ./godhead
COPY ./api ./api
RUN pip install --no-cache-dir fastapi uvicorn pyyaml requests mlflow web3 prometheus_client
CMD ["uvicorn", "api.model_api:app", "--host", "0.0.0.0", "--port", "8080"]
