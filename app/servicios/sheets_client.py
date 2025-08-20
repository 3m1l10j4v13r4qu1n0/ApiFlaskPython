import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from functools import wraps

# Configuración

# Cargar variables de entorno desde el archivo .env
load_dotenv()


# Ruta al archivo
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Archivo JSON de la cuenta de servicio de Google
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# En la URL de tu hoja de cálculo, el ID es la parte entre "/d/" y "/edit"
RANGE_NAME = os.getenv("RANGE_NAME")

def singleton(cls):
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

# 1. Interfaz


class ISheetsClient(ABC):
    """Interfaz abstracta para interactuar con Google Sheets."""

    @abstractmethod
    def read_range(self, range_name: str) -> List[List[Any]]:
        """Lee datos de un rango específico en Google Sheets."""
        pass

    @abstractmethod
    def write_range(self, range_name: str, values: List[List[Any]]) -> Dict:
        """Escribe datos en un rango específico."""
        pass

    @abstractmethod
    def append_rows(self, range_name: str, values: List[List[Any]]) -> Dict:
        """Agrega filas al final de un rango."""
        pass

    @abstractmethod
    def clear_range(self, range_name: str) -> Dict:
        """Limpia un rango específico."""
        pass

    


# 2. Implementación concreta

class GoogleSheetsClient(ISheetsClient):

    def __init__(self, credentials_file, spreadsheet_id):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self._service = None


    @property
    def service(self):
        """Propiedad que gestiona la conexión a la API (Lazy initialization)"""
        if self._service is None:
            scope = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope)
            self._service = build("sheets", "v4", credentials=creds)
        return self._service
    
    def read_range(self, range_name: str) -> List[List[Any]]:
        """
        Lee datos de un rango especificado.
        
        Parameters:
            range_name (str): Rango en formato 'Hoja1!A1:B2'
            
        Returns:
            List[List[Any]]: Lista de filas con los valores leídos
        """
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result.get("values", [])
    
    def write_range(self, range_name: str, values: List[List[Any]]) -> Dict:
        """
        Escribe datos en un rango especificado.
        
        Parameters:
            range_name (str): Rango en formato 'Hoja1!A1:B2'
            values (List[List[Any]]): Datos a escribir (lista de filas)
            
        Returns:
            Dict: Respuesta de la API
        """
        body = {"values": values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return result
    
    def append_rows(self, range_name: str, values: List[List[Any]]) -> Dict:
        """
        Añade filas al final de un rango especificado.
        
        Parameters:
            range_name (str): Rango en formato 'Hoja1!A1:B2'
            values (List[List[Any]]): Datos a añadir (lista de filas)
            
        Returns:
            Dict: Respuesta de la API
        """
        body = {"values": values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return result

    def clear_range(self, range_name: str) -> Dict:
        """
        Limpia el contenido de un rango especificado.
        
        Parameters:
            range_name (str): Rango en formato 'Hoja1!A1:B2'
            
        Returns:
            Dict: Respuesta de la API
        """
        result = self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result
