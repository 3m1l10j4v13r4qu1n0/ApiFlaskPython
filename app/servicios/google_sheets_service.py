
import os

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Configuración

# Cargar variables de entorno desde el archivo .env
load_dotenv()  

# Ruta al archivo
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  

# Archivo JSON de la cuenta de servicio de Google
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID") 

# En la URL de tu hoja de cálculo, el ID es la parte entre "/d/" y "/edit"
RANGE_NAME = os.getenv("RANGE_NAME")

# Rango a importar
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Función para convertir un DataFrame de pandas a una hoja de cálculo de Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE
                                                         , SCOPES)

# Construir el servicio de Google Sheets
SERVICE = build("sheets", "v4", credentials=creds)

# Clase GoogleSheetsService: -> devuelve un objeto 
# que permite interactuar con Google Sheets 
class GoogleSheetsService:
    def __init__(self, spreadsheet_id, range_name, service):
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.service = service

    def get_data(self):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name
        ).execute()
        return result.get("values", [])

    """
        Normaliza los datos de entrada para que coincidan con las columnas del modelo SQL.
        Si faltan columnas, se agregan con valor 'no_dato'.
        Si hay columnas adicionales, se eliminan.
    """
    def normalize_empty_cells(self,num_columns, data):
        normalized_rows = []
        for row in data:
        # Agrega 'no_dato' si faltan columnas
            extended_row = row + ['no_dato'] * (num_columns - len(row))
            normalized_rows.append(extended_row)
        # Reemplaza celdas vacías con 'no_dato'
        for i in range(len(normalized_rows)):
            normalized_rows[i] = ['no_dato' if cell == '' else cell for cell in normalized_rows[i]]
        return normalized_rows
     

"""
Clase para convertir los datos a un diccionario
"""
class DataToDict:
    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    def to_dict(self):
        if not self.data:
            return {}
        else:
            df = pd.DataFrame(self.data[1:], columns=self.data[0])
            return df.to_dict(orient='records')   

    

# Instanciar el servicio de Google Sheets
# Crear una instancia del servicio
google_sheets_service = GoogleSheetsService(SPREADSHEET_ID, RANGE_NAME
                                                            , SERVICE)
        
# Obtener los datos de la hoja de cálculo
data = google_sheets_service.get_data()
        
# Normalizar las celdas vacías
num_columns = len(data[0]) if data else 0

# lista de columnas
lista_columnas = data[0] if data else []

# Normalizar los datos
normalized_data = google_sheets_service.normalize_empty_cells(num_columns, data)

# Convertir los datos a un diccionario
lista_dict = DataToDict(normalized_data, lista_columnas)

# Convertir el DataFrame a un diccionario
data_dict = lista_dict.to_dict()

if __name__ == "__main__":
    print("Datos obtenidos de Google Sheets:")
    print(data_dict)
