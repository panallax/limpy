import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Configuración de la API
API_PREFIX = "/api"
API_TAGS = ["users"]
API_VERSION = "0.1.0"

