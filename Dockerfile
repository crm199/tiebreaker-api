FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY tiebreakers.py .
ENV SUPABASE_URL=https://gypbjlbuznipjrvbhlbg.supabase.co
ENV SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5cGJqbGJ1em5pcGpydmJobGJnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjY1NzUzNywiZXhwIjoyMDcyMjMzNTM3fQ.eIAQmlvcQQm9oP8E54XE2-Ez3WduDINtD_U3s51_YK8
ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]