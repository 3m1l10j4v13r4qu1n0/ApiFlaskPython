from .. import db


class Hijo(db.Model):
    """
    Modelo para representar un hijo de un afiliado en la base de datos.

    """

    __tablename__ = "HIJOS"
    id_hijo = db.Column(db.Integer, primary_key=True)
    id_afiliado = db.Column(
        db.Integer, db.ForeignKey("AFILIADOS.id_afiliado"), nullable=False
    )
    apellido = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    dni = db.Column(db.String, nullable=False)

    kits = db.relationship("Kit", backref="hijo", lazy=True)
