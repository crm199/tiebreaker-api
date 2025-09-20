import os
from dotenv import load_dotenv

# Load environment variables from PythonAnywhere or .env (local dev)
load_dotenv()

# Ensure critical env vars exist (you can still hardcode here for testing)
if not os.getenv("SUPABASE_URL"):
    os.environ["SUPABASE_URL"] = "https://gypbjlbuznipjrvbhlbg.supabase.co"

if not os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5cGJqbGJ1em5pcGpydmJobGJnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjY1NzUzNywiZXhwIjoyMDcyMjMzNTM3fQ.eIAQmlvcQQm9oP8E54XE2-Ez3WduDINtD_U3s51_YK8"

# Import the FastAPI app after env vars are ready
from main import app
