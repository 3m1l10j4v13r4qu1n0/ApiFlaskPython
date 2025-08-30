import os

from dotenv import load_dotenv
from app.servicios.sheets_service import SheetsService
from app.servicios.sheets_client import GoogleSheetsClient
from app.servicios.repository import GoogleSheetsRepository
from app.servicios.transformer import DataTransformer

# Cargar variables de entorno desde el archivo .env
load_dotenv()
# Ruta al archivo
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Archivo JSON de la cuenta de servicio de Google
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

RANGE_NAME = os.getenv("RANGE_NAME")

# Inicialización
client = GoogleSheetsClient(credentials_file=SERVICE_ACCOUNT_FILE, 
                            spreadsheet_id=SPREADSHEET_ID)
repo = GoogleSheetsRepository(client)

service = SheetsService(repo, DataTransformer())

lista_afiliados = service.get_normalized_data(range_name=RANGE_NAME)

if __name__ == "__main__":
    print("Cargar datos normalizados a la base de datos:")
    print(lista_afiliados[0]["afiliado"]["estado_civil"])  # Imprimir el primer afiliado normalizado
    