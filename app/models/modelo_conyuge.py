from .. import db


class Conyuge(db.Model):
    """
    Modelo para representar el conyuge de un afiliado en la base de datos.

    """

    __tablename__ = "CONYUGES"

    id = db.Column(db.Integer, primary_key=True)
    id_afiliado = db.Column(
        db.Integer, db.ForeignKey("AFILIADOS.id_afiliado"), nullable=False
    )

    # Atributos del conyuge
    nombre_apellido = db.Column(
        db.String(100), nullable=False
    )  # Nombre y apellido del conyuge
    fecha_nacimiento = db.Column(
        db.Date, nullable=False
    )  # Fecha de nacimiento del conyuge
    dni = db.Column(db.String(20), nullable=False, unique=True)  # DNI del conyuge

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
