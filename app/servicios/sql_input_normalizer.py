from datetime import datetime

from google_sheets_service import data_dict, lista_columnas
"""
Clase para normalizar los datos de entrada de modelos de SQL

"""
class SQLInputNormalizer:
 
    def __init__(self, ram_data: dict, columns: list) -> dict:
        self.ram_data = ram_data
        self.columns = columns
        self.models = {
            "afiliado": {},
            "conyuge": {},
            "hijos": []
        }

    """
        Normaliza los datos de entrada para que coincidan con las columnas del modelo SQL.
    """
    def normalize_input(self):
        for column in self.columns:
            self.normalize_afiliado(column)
            self.normalize_conyuge(column)
            self.normalize_hijos(column)
            # Agrega otros modelos según sea necesario
        return self.models
    
    def normalize_afiliado(self, column):
        column = column
        columna_afiliado = self.columns[0:20]
        if column in columna_afiliado:
            self.models["afiliado"][column] = self.ram_data[column]
        
    def normalize_conyuge(self, column):
        column = column
        columna_conyuge = self.columns[20:24]
        if column in columna_conyuge:
            if column == "Nombre y Apellido ( Conyuge ) :":
                if self.ram_data[column] != 'no_dato':
                    self.models["conyuge"]["Nombre y Apellido"] = self.ram_data[column]
        
            elif column == "Fecha de Nacimiento ( Conyuge ) :":
                    if self.ram_data[column] != 'no_dato':    
                        self.models["conyuge"]["Fecha de Nacimiento"] = self.ram_data[column]
            elif column == "DNI ( Conyuge ) :":
                if self.ram_data[column] != 'no_dato':
                    self.models["conyuge"]["DNI"] = self.ram_data[column]
            
    
    def normalize_hijos(self, column):
        column = column
        columna_hijos = self.columns[25:-1]
        if column in columna_hijos:
            hijo = {
                "Nombre y Apellido": None,
                "Fecha de Nacimiento": None,
                "DNI": None
            }
            # Normaliza los datos de los hijos
            for i in range(0,7): # Recorre los hijos del 1 al 7
                # Asigna los valores a los campos correspondientes
                if column == f"Nombre y Apellido ( Hijo {i+1} ) :":
                    if self.ram_data[column] != 'no_dato':
                        hijo["Nombre y Apellido"] = self.ram_data[column]
                elif column == f"Fecha de Nacimiento ( Hijo {i+1} ) :":
                    if self.ram_data[column] != 'no_dato':
                        hijo["Fecha de Nacimiento"] = self.ram_data[column]
                elif column == f"DNI ( Hijo {i+1} ) :":
                    if self.ram_data[column] != 'no_dato':
                        hijo["DNI"] = self.ram_data[column]
            # Si el hijo tiene datos, lo agrega a la lista de hijos
            self.models["hijos"].append(hijo)
                    
                        
            

                    

            

# Instaciar modelo de normalización
sql_input_normalizer = SQLInputNormalizer(data_dict[0], lista_columnas)

if __name__ == "__main__":
    # Ejemplo de uso
    print("Datos normalizados:")
    #print(sql_input_normalizer.normalize_input())
    #print(sql_input_normalizer.normalize_input()["conyuge"])
    print(sql_input_normalizer.normalize_input()["hijos"]) 
