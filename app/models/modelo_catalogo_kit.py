from .. import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields

class Kit(db.Model):
    """
    Modelo para representar un kit asignado a un hijo.

    """

    __tablename__ = "KITS"
    id_kit = db.Column(db.Integer, primary_key=True)
    id_hijo = db.Column(db.Integer, db.ForeignKey("HIJOS.id"), nullable=False)
    tipo_kit = db.Column(
        db.String, db.ForeignKey("CATALOGO_KITS.tipo_kit"), nullable=False
    )


class CatalogoKit(db.Model):
    """
    Modelo para representar el catálogo de kits disponibles.

    """

    __tablename__ = "CATALOGO_KITS"
    tipo_kit = db.Column(db.String, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    edad_min = db.Column(db.Integer, nullable=False)
    edad_max = db.Column(db.Integer, nullable=False)
    contiene = db.Column(db.String, nullable=False)

    kits = db.relationship("Kit", backref="catalogo", lazy=True)


# Schema para serialización y deserialización
class CatalogoKitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CatalogoKit
        load_instance = True
        include_relationships = True

    
class KitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Kit
        load_instance = True
        include_fk = True

    catalogo = fields.Nested(CatalogoKitSchema)


