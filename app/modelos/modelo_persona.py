from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from utils.enumeraciones import Genero, EstadoCivil


# Clase base Persona
@dataclass
class Persona:
    id: int
    apellido: str
    nombre: str
    dni: str
    fecha_nacimiento: date
    edad: int = field(init=False)  # No se inicializa en el constructor
    genero: Genero

    def __post_init__(self):
        # Calcula la edad automáticamente al crear la instancia
        self.edad = self.calcular_edad()

    def calcular_edad(self) -> int:
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year

        # Verificar si ya cumplió años este año
        if (hoy.month < self.fecha_nacimiento.month) or (
            hoy.month == self.fecha_nacimiento.month and hoy.day < self.fecha_nacimiento.day
        ):
            edad -= 1  # Aún no ha cumplido años este año

        return edad


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
        genero=Genero.MASCULINO.name,
    )

    conyuge1 = Conyuge(
        id=2,
        apellido="Gómez",
        nombre="María",
        dni="87654321",
        fecha_nacimiento=date(1985, 8, 20),
        genero=Genero.FEMENINO.name,
    )

    hijo1 = Hijo(
        id=3,
        apellido="Pérez",
        nombre="Carlos",
        dni="13579246",
        fecha_nacimiento=date(2010, 3, 10),
        genero=Genero.MASCULINO.name,
    )

    hijo2 = Hijo(
        id=4,
        apellido="Pérez",
        nombre="Laura",
        dni="24681357",
        fecha_nacimiento=date(2012, 7, 25),
        genero = Genero.FEMENINO.name,
    )

    afiliado1 = Afiliado(
        id=1,
        apellido="Pérez",
        nombre="Juan",
        dni="12345678",
        fecha_nacimiento=date(1980, 5, 15),
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
    

    print("\nCónyuge del afiliado:")
    print(afiliado1.conyuge)

    print("\nHijos del afiliado:")
    for hijo in afiliado1.hijos:
        print(hijo)
    print(type(afiliado1.genero.name))
        