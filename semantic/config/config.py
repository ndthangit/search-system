from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    ELASTIC_URL: str = os.getenv("ELASTIC_URL")
    ELASTIC_USERNAME: str = os.getenv("ELASTIC_USERNAME")
    ELASTIC_PASSWORD: str = os.getenv("ELASTIC_PASSWORD")
    ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES: str = os.getenv("ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES")

settings = Settings()
# print(settings)