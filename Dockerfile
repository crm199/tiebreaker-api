FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# Use exec form to ensure $PORT is resolved by the shell
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}