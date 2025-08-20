from typing import List, Dict, Any
from .sql_input_normalized import SQLInputNormalized

# DataTransformer

class DataTransformer:
    """ 
    Clase para transformar datos obtenidos de Google Sheets en un formato normalizado.

    Methods:
        normalize_empty(raw_data, default): Normaliza los datos reemplazando celdas vacías
        to_dicts(raw_data, headers): Convierte una lista de listas en una lista de diccionarios
    """

    @staticmethod
    def normalize_empty(raw_data: List[List[Any]], num_columns: int ) -> List[List[Any]]:
        """
        Normaliza los datos reemplazando celdas vacías con un valor por defecto
        
        Parameters:
            raw_data: List[List[Any]] - Datos en formato de lista de listas (filas y columnas)
            num_columns: int - Número de columnas esperadas en cada fila
            
        Return:
            List[Dict[str, Any]] - Datos normalizados en formato de lista de diccionarios
    
        """
        normalized_rows = []
        for row in raw_data:
            # Agrega 'no_dato' si faltan columnas
            extended_row = row + ["no_dato"] * (num_columns - len(row))
            normalized_rows.append(extended_row)
        # Reemplaza celdas vacías con 'no_dato'
        for i in range(len(normalized_rows)):
            normalized_rows[i] = [
                "no_dato" if cell == "" else cell for cell in normalized_rows[i]
            ]
        return normalized_rows
        
    @staticmethod
    def to_dicts(raw_data: List[List[Any]], headers: List[str]) -> List[Dict[str, Any]]:
        """
        Convierte una lista de listas en una lista de diccionarios utilizando los encabezados proporcionados
        
        Parameters:
            raw_data: List[List[Any]] - Datos en formato de lista de listas (filas y columnas)
            headers: List[str] - Encabezados para las columnas
        Returns:
            List[Dict[str, Any]] - Datos convertidos en formato de lista de diccionarios
        """
        return [dict(zip(headers, row)) for row in raw_data]
    
    @staticmethod
    def normalize_input(dicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normaliza la entrada de datos para ser compatible con SQL
        
        Parameters:
            dicts: List[Dict[str, Any]] - Datos en formato de lista de diccionarios
        Returns:
            lista_normalizada: List[Dict[str, Any]] - Datos normalizados para SQL
        """
        lista_normalizada = []

        for row in range(len(dicts)):
            # Crear una instancia de SQLInputNormalizer para cada fila
            extended_row = SQLInputNormalized(ram_data=dicts[row])
            # Normalizar la entrada
            lista_normalizada.append(extended_row.normalize_input())

        return lista_normalizada
    
    
    
   