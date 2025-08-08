from .. import db


class Hijo(db.Model):
    """
    Modelo para representar un hijo de un afiliado en la base de datos.

    """

    __tablename__ = "HIJOS"
    id_hijo = db.Column(db.Integer, primary_key=True)
    id_afiliado = db.Column(
        db.Integer, db.ForeignKey("AFILIADOS.id"), nullable=False
    )
    nombre_apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    dni = db.Column(db.String(20), nullable=False)

    kits = db.relationship("Kit", backref="hijo", lazy=True)
