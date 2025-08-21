class SQLInputNormalized:
    """
    Clase para normalizar los datos de entrada de modelos de SQL.

    Parameters:
        ram_data(dict): Datos de entrada del modelo SQL.

    Methods:
        normalize_input(): Normaliza los datos de entrada del modelo SQL.
        normalize_afiliado(): Normaliza los datos del afiliado.
        normalize_conyuge(): Normaliza los datos del cónyuge.
        normalize_hijos(): Normaliza los datos de los hijos.


    Returns:
        models(dict): Diccionario con los datos normalizados.

    """

    def __init__(self, ram_data: dict) -> dict:
        self.ram_data = ram_data
        self.afiliado = {
            "afiliado": {},
            "conyuge": {},
            "hijos": []
        }

    def normalize_input(self):
        self.normalize_afiliado()
        self.normalize_conyuge()
        self.normalize_hijos()
        return self.afiliado
    
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
                # Si el valor no es "no_dato", lo agregamos al diccionario
                self.afiliado[models_name][new_key] = valor


    def normalize_afiliado(self):
        """ Normaliza los datos del afiliado.
        Mapea las claves del afiliado a un formato normalizado.
        Asegúrate de que las claves coincidan con las de tu hoja de cálculo.
        """
        # Mapeo de claves del afiliado
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
            "Titulo / Carrera:": "titulo_obtenido",
            "N° De Legajo:": "numero_legajo",
            "Comuna del sendero donde trabaja:": "comuna_donde_trabaja",
            "Inicio Actividad en Prevención:": "fecha_ingreso",
            "Relación de Dependencia:": "relacion_dependencia",
            }
        self.add_new_key(mapping, "afiliado")

    def normalize_conyuge(self):
        """ Normaliza los datos del cónyuge.
        Mapea las claves del cónyuge a un formato normalizado.
        Asegúrate de que las claves coincidan con las de tu hoja de cálculo.
        """
        # Mapeo de claves del cónyuge
        # Asegúrate de que las claves coincidan con las de tu hoja de cálculo
        mapping = {
            "Nombre y Apellido ( Conyuge ) :": "nombre_apellido",
            "Fecha  de Nacimiento ( Conyuge ) :": "fecha_nacimiento",
            "D.n.i ( Conyuge ) :": "dni",
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
                self.afiliado["hijos"].append(hijo)

            

