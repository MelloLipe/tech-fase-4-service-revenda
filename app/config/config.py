import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Revenda Veiculos - Servico Principal"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./main_service.db")
    SALES_SERVICE_URL: str = os.getenv("SALES_SERVICE_URL", "http://localhost:8001")


settings = Settings()
