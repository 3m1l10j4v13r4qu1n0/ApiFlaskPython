from .. import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields


class Hijo(db.Model):
    """
    Modelo para representar un hijo de un afiliado en la base de datos.

    """

    __tablename__ = "HIJOS"
    id = db.Column(db.Integer, primary_key=True)
    id_afiliado = db.Column(
        db.Integer, db.ForeignKey("AFILIADOS.id"), nullable=False
    )
    nombre_apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    dni = db.Column(db.String(20), nullable=False)

# Schema para serialización y deserialización
class HijoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hijo
        load_instance = True
        include_fk = True
    fecha_nacimiento = fields.Date(format="%d/%m/%Y")
    
    kits = fields.Nested('KitSchema', many=True)

