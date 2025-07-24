
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Configuración
load_dotenv()  # Cargar variables de entorno desde el archivo .env
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Ruta al archivo
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID") # En la URL de tu hoja
RANGE_NAME = os.getenv("RANGE_NAME")# Rango a importar

creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
service = build("sheets", "v4", credentials=creds)


# Leer datos
result = service.spreadsheets().values().get(
    spreadsheetId= SPREADSHEET_ID,
    range= RANGE_NAME
).execute()
print(result.get("values", []))