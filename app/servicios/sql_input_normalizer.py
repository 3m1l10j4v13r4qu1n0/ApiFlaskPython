from google_sheets_service import data_dict, lista_columnas


class SQLInputNormalizer:
    """
    Clase para normalizar los datos de entrada de modelos de SQL.

    Parameters:
        ram_data(dict): Datos de entrada del modelo SQL.
        columns(list): Lista de columnas esperadas en el modelo SQL.

    Methods:
        normalize_input(): Normaliza los datos de entrada del modelo SQL.
        normalize_afiliado(): Normaliza los datos del afiliado.
        normalize_conyuge(): Normaliza los datos del cónyuge.
        normalize_hijos(): Normaliza los datos de los hijos.


    Returns:
        models(dict): Diccionario con los datos normalizados.

    """

    def __init__(self, ram_data: dict, columns: list) -> dict:
        self.ram_data = ram_data
        self.columns = columns
        self.models = {"afiliado": {}, "conyuge": {}, "hijos": []}

    def normalize_input(self):
        self.normalize_afiliado()
        self.normalize_conyuge()
        self.normalize_hijos()
        return self.models

    def normalize_afiliado(self):
        for column in self.columns[0:20]:
            self.models["afiliado"][column] = self.ram_data.get(column, None)

    def normalize_conyuge(self):
        mapping = {
            "Nombre y Apellido ( Conyuge ) :": "Nombre y Apellido",
            "Fecha de Nacimiento ( Conyuge ) :": "Fecha de Nacimiento",
            "DNI ( Conyuge ) :": "DNI",
        }
        for key, new_key in mapping.items():
            valor = self.ram_data.get(key, "no_dato")
            if valor != "no_dato":
                self.models["conyuge"][new_key] = valor

    def normalize_hijos(self):
        for i in range(1, 8):  # Hijo 1 al 7
            hijo = {
                "Nombre y Apellido": self.ram_data.get(
                    f"Apellido/s y Nombre/s  hijo/a {i}", "no_dato"
                ),
                "Fecha de Nacimiento": self.ram_data.get(
                    f"Fecha nacimiento hijo/a {i}", "no_dato"
                ),
                "DNI": self.ram_data.get(f"D.n.i hijo/a {i}", "no_dato"),
            }
            # Solo agregamos si al menos un dato no es 'no_dato'
            if any(v != "no_dato" for v in hijo.values()):
                self.models["hijos"].append(hijo)


def normalize_list(lista_data: list, lista_columnas: list) -> list:
    """
    Función para normalizar una lista de datos.

    Parameters:
        lista_data(list): Lista de datos a normalizar.
        lista_columnas(list): Lista de columnas esperadas en el modelo SQL.

    Methods:
        normalize_input(): Normaliza los datos de entrada del modelo SQL.

    Returns:
        lista_normalizada(list): Lista de datos normalizados.
    """
    lista_data = lista_data
    lista_columnas = lista_columnas
    lista_normalizada = []

    for row in range(len(lista_data)):
        extended_row = SQLInputNormalizer(lista_data[row], lista_columnas)
        # Crear una fila extendida
        lista_normalizada.append(extended_row.normalize_input())

    return lista_normalizada


if __name__ == "__main__":
    # Ejemplo de uso
    print("Datos normalizados:")
    print(normalize_list(data_dict, lista_columnas))
