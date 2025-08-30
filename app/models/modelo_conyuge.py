from .. import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields

class Conyuge(db.Model):
    """
    Modelo para representar el conyuge de un afiliado en la base de datos.

    """

    __tablename__ = "CONYUGES"

    id = db.Column(db.Integer, primary_key=True)
    id_afiliado = db.Column(
        db.Integer, db.ForeignKey("AFILIADOS.id"), nullable=False
    )

    # Atributos del conyuge
    nombre_apellido = db.Column(
        db.String(100), nullable=False
    )  # Nombre y apellido del conyuge
    fecha_nacimiento = db.Column(
        db.Date, nullable=False
    )  # Fecha de nacimiento del conyuge
    dni = db.Column(db.String(20), nullable=False, unique=True)  # DNI del conyuge

   
# Schema para serialización y deserialización
class ConyugeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Conyuge
        load_instance = True
        include_fk = True
    fecha_nacimiento = fields.Date(format="%d/%m/%Y")
    id_afiliado = fields.Int(dump_only=True)  # 👈 no requerido en input JSON
    