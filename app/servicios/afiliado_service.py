#from typing import Dict, List
from .. import db

#from ..models.modelo_catalogo_kit import Kit, CatalogoKit, KitSchema, CatalogoKitSchema
from ..models.modelo_conyuge import Conyuge, ConyugeSchema
from ..models.modelo_hijo import Hijo, HijoSchema
from ..models.modelo_afiliado import Afiliado, AfiliadoSchema




class AfiliadoService:
    def __init__(self):
        self.schema = AfiliadoSchema()

    def crear_afiliado(self, data: dict) -> Afiliado:
        """
        Recibe un dict (JSON) y crea un afiliado en la base de datos.
        """
        # 1. Deserializar el dict → instancia de Afiliado
        afiliado = self.schema.load(data, session=db.session)

        # 2. Guardar en DB
        db.session.add(afiliado)
        db.session.commit()

        return afiliado

    def obtener_afiliado(self, id: int) -> dict:
        """
        Recupera un afiliado de la DB y lo serializa a dict.
        """
        afiliado = Afiliado.query.get_or_404(id)
        return self.schema.dump(afiliado)

    def listar_afiliados(self) -> list:
        """
        Devuelve todos los afiliados como lista de dicts.
        """
        afiliados = Afiliado.query.all()
        return self.schema.dump(afiliados, many=True)





class ConyugeService:

    def __init__(self):
        self.schema = ConyugeSchema()

    def crear_conyuge(self, afiliado_id: int, data: dict) -> Conyuge:
        """
        Crea un cónyuge y lo asocia a un afiliado.
        """
        afiliado = Afiliado.query.get_or_404(afiliado_id)

        # Usamos la relación ORM (afiliado.conyuges.append)
        conyuge = self.schema.load(data, session=db.session)
        afiliado.conyuges.append(conyuge)

        db.session.add(afiliado)  # cascada guarda el cónyuge
        db.session.commit()
        return conyuge

    def obtener_conyuge(self, id: int) -> dict:
        conyuge = Conyuge.query.get_or_404(id)
        return self.schema.dump(conyuge)

    def listar_conyuges(self, afiliado_id: int = None) -> list:
        if afiliado_id:
            conyuges = Conyuge.query.filter_by(id_afiliado=afiliado_id).all()
        else:
            conyuges = Conyuge.query.all()
        return self.schema.dump(conyuges, many=True)


    


class HijoService:

    def __init__(self):
        self.schema = HijoSchema()

    def crear_hijo(self, afiliado_id: int, data: dict) -> Hijo:
        """
        Crea un hijo y lo asocia a un afiliado.
        """
        afiliado = Afiliado.query.get_or_404(afiliado_id)

        hijo = self.schema.load(data, session=db.session)
        afiliado.hijos.append(hijo)

        db.session.add(afiliado)  # cascada guarda el hijo
        db.session.commit()
        return hijo

    def obtener_hijo(self, id: int) -> dict:
        hijo = Hijo.query.get_or_404(id)
        return self.schema.dump(hijo)

    def listar_hijos(self, afiliado_id: int = None) -> list:
        if afiliado_id:
            hijos = Hijo.query.filter_by(id_afiliado=afiliado_id).all()
        else:
            hijos = Hijo.query.all()
        return self.schema.dump(hijos, many=True)




class FactoryAfiliado:
    def __init__(self):
        self.afiliado_service = AfiliadoService()
        self.conyuge_service = ConyugeService()
        self.hijo_service = HijoService()

    def crear_afiliado_completo(self, data: dict):
        """
        Crea un afiliado con sus relaciones (conyuge e hijos).
        El `data` debe tener esta estructura:
        {
            "afiliado": {...},
            "conyuge": {...},
            "hijos": [{...}, {...}]
        }
        """
        try:
            # 1. Crear afiliado
            afiliado_data = data.get("afiliado")
            afiliado = self.afiliado_service.crear_afiliado(afiliado_data)

            # 2. Crear cónyuge (si existe)
            conyuge_data = data.get("conyuge")
            if conyuge_data:
                self.conyuge_service.crear_conyuge(afiliado.id, conyuge_data)

            # 3. Crear hijos (si existen)
            hijos_data = data.get("hijos", [])
            for hijo_data in hijos_data:
                self.hijo_service.crear_hijo(afiliado.id, hijo_data)

            return {"status": "ok", "id_afiliado": afiliado.id}

        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}
        



