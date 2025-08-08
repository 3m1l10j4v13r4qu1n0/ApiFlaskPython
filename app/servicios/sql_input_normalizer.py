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
    
    def add_new_key(self, mapping: dict, models_name: str) -> None:
        """
        Método para cambiar el nombre de las claves en el diccionario de datos.

        Parameters:
            mapping(dict): Diccionario que contiene las claves originales y sus nuevos nombres.
            models_name(str): Nombre del modelo al que se le asignarán los nuevos nombres de claves

        Returns:
            None: Modifica el diccionario de datos en la clase directamente.    
        """
        for key, new_key in mapping.items():
            valor = self.ram_data.get(key, "no_dato")
            if valor != "no_dato":
                self.models[models_name][new_key] = valor


    def normalize_afiliado(self):
        mapping = {
            "Marca temporal": "marca_temporal_creacion",
            "Apellido/s:": "apellido",
            "Nombre/s:": "nombre",
            "Fecha de Nacimiento:": "fecha_nacimiento",
            "D.N.I:": "dni",
            "Tel Contacto:": "telefono",
            "Email:": "email",
            "Nacionalidad:": "nacionalidad",
            "Género:": "genero",
            "Estado Civil:": "estado_civil",
            "Domicilio (Calle y n°):": "direccion",
            "Localidad:": "localidad",
            "Provincia:": "provincia",
            "Codigo Postal:": "codigo_postal",
            "Estudios:": "nivel_educativo",
            "Titulo / Carrera:": "titulo_obtenid",
            "N° De Legajo:": "numero_legajo",
            "Comuna del sendero donde trabaja:": "comuna_donde_trabaja",
            "Inicio Actividad en Prevención:": "fecha_ingreso",
            "Relación de Dependencia:": "relacion_dependencia",
            }
        self.add_new_key(mapping, "afiliado")


    def normalize_conyuge(self):
        mapping = {
            "Nombre y Apellido ( Conyuge ) :": "nombre_apellido",
            "Fecha de Nacimiento ( Conyuge ) :": "fecha_nacimiento",
            "DNI ( Conyuge ) :": "dni",
        }
        self.add_new_key(mapping, "conyuge")

    def normalize_hijos(self):
        for i in range(1, 8):  # Hijo 1 al 7
            hijo = {
                "nombre_apellido": self.ram_data.get(
                    f"Apellido/s y Nombre/s  hijo/a {i}", "no_dato"
                ),
                "fecha_nacimiento": self.ram_data.get(
                    f"Fecha nacimiento hijo/a {i}", "no_dato"
                ),
                "dni": self.ram_data.get(f"D.n.i hijo/a {i}", "no_dato"),
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
