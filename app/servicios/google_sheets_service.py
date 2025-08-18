import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any, Optional
from functools import wraps
from .sql_input_normalizer import SQLInputNormalizer

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





@singleton
class GoogleSheetsClient:
    """Cliente para interactuar con Google Sheets API respetando principios SOLID"""
    
    def __init__(self, service_account_file: str, spreadsheet_id: str):
        """
        Inicializa el cliente con las credenciales y el ID de la hoja.
        
        Args:
            credentials_file (str): Ruta al archivo JSON de credenciales
            spreadsheet_id (str): ID de la hoja de cálculo de Google Sheets
        """
        self.credentials_file = service_account_file
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
        
        Args:
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
        
        Args:
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
        
        Args:
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
        
        Args:
            range_name (str): Rango en formato 'Hoja1!A1:B2'
            
        Returns:
            Dict: Respuesta de la API
        """
        result = self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result






class FactoryGoogleSheetsService:
    """
    Clase FactoryGoogleSheetsService -> crea una instancia del servicio de Google Sheets
    y proporciona métodos para interactuar con la hoja de cálculo.

    """


    def __init__(self):
        self.data = self.get_data(RANGE_NAME) # Obtener datos de la hoja de cálculo
        if not self.data :
            raise ValueError("No se encontraron datos en la hoja de calculo.")
        self.normalize_data = self.normalize_empty_cells(num_columns=len(self.data[0]))
        if not self.normalize_data:
            raise ValueError("No se encontraron datos en la hoja de calculo normalizados.")

    # Crear instancia del cliente
    @property
    def sheets_client(self, service_account_file: Optional[str] ="service_account_file", 
                      spreadsheet_id: Optional[str] = "spreadsheet_id" ) -> GoogleSheetsClient:
        """        Propiedad que crea una instancia del cliente de Google Sheets.   
        Args:
            service_account_file (str): Ruta al archivo de credenciales
            spreadsheet_id (str): ID de la hoja de cálculo
        Returns:
            GoogleSheetsClient: Instancia del cliente de Google Sheets
        """
        if not service_account_file or not spreadsheet_id:
            raise ValueError("El archivo de credenciales y el ID de la hoja de cálculo son obligatorios.")
        try:    
            _sheets_client = GoogleSheetsClient(SERVICE_ACCOUNT_FILE,
                                                SPREADSHEET_ID) 
        except Exception as e:
            print(f"Error al crear el cliente de Google Sheets: {e}")
            _sheets_client = None
        return _sheets_client
    
    
    def get_data(self,range_name: str) -> List[List[Any]]:
        """
        Obtiene los datos del rango especificado en la hoja de cálculo.
        
        Returns:
            List[List[Any]]: Lista de listas con los datos obtenidos.
        """
        try:
            if not range_name:
                raise ValueError("El rango no puede estar vacío.")
        except ValueError as e:
            print(f"Error: {e}")
            return []
        return self.sheets_client.read_range(range_name)

    def normalize_empty_cells(self, num_columns: int)-> list:
    
        normalized_rows = []
        for row in self.data:
            # Agrega 'no_dato' si faltan columnas
            extended_row = row + ["no_dato"] * (num_columns - len(row))
            normalized_rows.append(extended_row)
        # Reemplaza celdas vacías con 'no_dato'
        for i in range(len(normalized_rows)):
            normalized_rows[i] = [
                "no_dato" if cell == "" else cell for cell in normalized_rows[i]
            ]
        return normalized_rows
    
    def convertir_a_lista(self) -> List[Dict[str, Any]]:
        """
        Convierte los datos normalizados a una lista de diccionarios.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos normalizados.
        """
        lista = []
        # Convertir los datos a una lista de diccionarios
        sin_primera_fila = self.normalize_data[1:] if len(self.normalize_data) > 1 else []
        if not sin_primera_fila:
            raise ValueError("No se encontraron datos en la hoja de calculo normalizados.")
        # Convertir los datos a una lista de diccionarios
        for i in range(len(sin_primera_fila)):
            # Crear una instancia de ConvertirALista para cada fila
            d = ConvertirALista(raw_data=sin_primera_fila,columns=self.data[0]).to_dict(iterador=i)
            lista.append(d)
        return lista
    
    def normalizer_list(self) -> List[Dict[str, Any]]:
        """ 
        Normaliza la lista de diccionarios obtenidos de la hoja de cálculo. 
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios normalizados.
        """

        lista = self.convertir_a_lista()
        lista_normalizada = []

        for row in range(len(lista)):
            # Crear una instancia de SQLInputNormalizer para cada fila
            extended_row = SQLInputNormalizer(ram_data=lista[row], columns=self.data[0])
            # Normalizar la entrada
            lista_normalizada.append(extended_row.normalize_input())

        return lista_normalizada
    
    def __repr__(self):
        return f"{self.normalizer_list()}"
    



class ConvertirALista:
    """
    Clase CovertirALista -> devuelve una lista con Diccionarios con 
    los datos de la hoja de google.

    Parameters:
        raw_data(list) lista de los datos de la hoja de google
        columns(lista) lista de las columnas.

    Methods:
        to_dict() Convierte los datos a una lista de diccionario.

    Returns:
        retorna una lista de diccionarios de los datos.
    
    """

    def __init__(self, raw_data:list, columns) -> list:
        self.raw_data = raw_data
        self.columns = columns
       
    def to_dict(self, iterador: int):
        if len(self.raw_data[iterador]) != len(self.columns):
            raise ValueError("las lista deben terner la misma longitud")
        return dict(zip(self.columns,self.raw_data[iterador])) 
    
    def to_list(self):
        lista = []
        for i in range(len(self.raw_data)):
            d = self.to_dict(iterador=i)
            lista.append(d)
        return lista

            
        
if __name__ == "__main__":
    print("Datos obtenidos de Google Sheets:")
    lista_afiliados = FactoryGoogleSheetsService().normalizer_list()
    