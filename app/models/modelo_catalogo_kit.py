from .. import db


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


class Kit(db.Model):
    """
    Modelo para representar un kit asignado a un hijo.

    """

    __tablename__ = "KITS"
    id_kit = db.Column(db.Integer, primary_key=True)
    id_hijo = db.Column(db.Integer, db.ForeignKey("HIJOS.id_hijo"), nullable=False)
    tipo_kit = db.Column(
        db.String, db.ForeignKey("CATALOGO_KITS.tipo_kit"), nullable=False
    )
