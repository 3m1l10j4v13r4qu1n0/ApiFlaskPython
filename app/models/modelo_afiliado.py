from .. import db


class Afiliado(db.Model):
    """
    Modelo para representar un afiliado en la base de datos.

    """

    __tablename__ = "AFILIADOS"

    id = db.Column(db.Integer, primary_key=True)
    # Atributos del afiliado
    # Datos personales
    apellido = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)
    nacionalidad = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(10), nullable=False)  # 'Masculino', 'Femenino', etc.
    estado_civil = db.Column(db.String(20), nullable=False)  # 'Soltero', 'Casado', etc.

    # Domicilio
    provincia = db.Column(db.String(50), nullable=False)
    localidad = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)

    # Educación
    nivel_educativo = db.Column(
        db.String(50), nullable=False
    )  # 'Primaria', 'Secundaria', 'Terciario', 'Universitario', etc.
    titulo_obtenido = db.Column(
        db.String(100), nullable=True
    )  # Título obtenido, si aplica

    # Datos laborales
    numero_legajo = db.Column(
        db.String(50), nullable=False, unique=True
    )  # Número de legajo del afiliado
    fecha_ingreso = db.Column(db.Date, nullable=False)  # Fecha de ingreso al trabajo
    comuna_donde_trabaja = db.Column(
        db.String(50), nullable=False
    )  # Comuna donde trabaja
    relacion_dependencia = db.Column(
        db.String(50), nullable=False
    )  # 'monotributista', 'planta_transitoria', 'planta_permanente'

    # Marca temporal de creación y actualización
    marca_temporal_creacion = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    marca_temporal_actualizacion = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relaciones con otros modelos
    conyuges = db.relationship("Conyuge", backref="afiliado", lazy=True)
    hijos = db.relationship("Hijo", backref="afiliado", lazy=True)
