from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from enum import Enum, auto

# Enumeraciones
class Genero(Enum):
    MASCULINO=auto()
    FEMENINO=auto()
    OTRO=auto()

class EstadoCivil(Enum):
    SOLTERO=auto()
    CASADO=auto()
    DIVORCIADO=auto()

# Clase base Persona
@dataclass
class Persona:
    id: int
    apellido: str
    nombre: str
    dni: str
    fecha_nacimiento: date
    edad: int
    genero: Genero

# Clase PersMayor que hereda de Persona
@dataclass
class PersMayor(Persona):
    tel_contacto: str
    email: str
    estado_civil: EstadoCivil

# Clase Afiliado que hereda de PersMayor
@dataclass
class Afiliado(PersMayor):
    conyuge: Optional["Conyuge"]=None
    hijos: List["Hijo"]=field(default_factory=list)

# Clase Conyuge que hereda de Persona
@dataclass
class Conyuge(Persona):
    pass

# Clase Hijo que hereda de Persona
@dataclass
class Hijo(Persona):
    pass

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancias
    persona1 = Persona(
        id=1,
        apellido="Pérez",
        nombre="Juan",
        dni="12345678",
        fecha_nacimiento = date(1980, 5, 15),
        edad=43,
        genero=Genero.MASCULINO,
    )

    conyuge1 = Conyuge(
        id=2,
        apellido="Gómez",
        nombre="María",
        dni="87654321",
        fecha_nacimiento=date(1985, 8, 20),
        edad=38,
        genero=Genero.FEMENINO.name,
    )

    hijo1 = Hijo(
        id=3,
        apellido="Pérez",
        nombre="Carlos",
        dni="13579246",
        fecha_nacimiento=date(2010, 3, 10),
        edad=13,
        genero=Genero.MASCULINO.name,
    )

    hijo2 = Hijo(
        id=4,
        apellido="Pérez",
        nombre="Laura",
        dni="24681357",
        fecha_nacimiento = date(2012, 7, 25),
        edad=11,
        genero = Genero.FEMENINO.name,
    )

    afiliado1 = Afiliado(
        id=1,
        apellido="Pérez",
        nombre="Juan",
        dni="12345678",
        fecha_nacimiento = date(1980, 5, 15),
        edad = 43,
        genero = Genero.MASCULINO,
        tel_contacto = "+541112345678",
        email = "juan.perez@example.com",
        estado_civil = EstadoCivil.CASADO.name,
        conyuge = conyuge1,
        hijos=[hijo1, hijo2],
    )

    # Mostrar información
    print("Afiliado:")
    print(afiliado1)
"""
    print("\nCónyuge del afiliado:")
    print(afiliado1.conyuge)

    print("\nHijos del afiliado:")
    for hijo in afiliado1.hijos:
        print(hijo)
        """