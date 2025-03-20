from enum import Enum,auto

#Enumenraciones
#opciones de genero

class Genero(Enum):
    MASCULINO=auto()
    FEMENINO=auto()
    OTRO=auto()

#opciines de Estado civil

class EstadoCivil(Enum):
    SOLTERO=auto()
    CASADO=auto()
    DIVORCIADO=auto()
        


