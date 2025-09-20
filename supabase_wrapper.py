import os
from dotenv import load_dotenv
from asgiref.wsgi import ASGItoWSGI  # <-- import adapter

# Load env vars
load_dotenv()

if not os.getenv("SUPABASE_URL"):
    os.environ["SUPABASE_URL"] = "https://gypbjlbuznipjrvbhlbg.supabase.co"

if not os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5cGJqbGJ1em5pcGpydmJobGJnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjY1NzUzNywiZXhwIjoyMDcyMjMzNTM3fQ.eIAQmlvcQQm9oP8E54XE2-Ez3WduDINtD_U3s51_YK8"

# Import FastAPI app AFTER env vars
from main import app

# Wrap FastAPI (ASGI) into WSGI for PythonAnywhere
application = ASGItoWSGI(app)
