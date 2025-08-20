import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify
from ..servicios.sheets_service import SheetsService
from ..servicios.repository import GoogleSheetsRepository
from ..servicios.transformer import DataTransformer
from ..servicios.sheets_client import GoogleSheetsClient
#from ..models.afiliado import Afiliado, Conyuge
from .. import db

# Cargar variables de entorno
load_dotenv()

# Ruta al archivo
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Archivo JSON de la cuenta de servicio de Google
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

RANGE_NAME = os.getenv("RANGE_NAME")

# Definir el Blueprint
afiliados_bp = Blueprint("afiliados", __name__, url_prefix="/api/afiliados")

# Instanciar cliente y servicio
# Inicialización
client = GoogleSheetsClient(credentials_file=SERVICE_ACCOUNT_FILE, 
                            spreadsheet_id=SPREADSHEET_ID)
repo = GoogleSheetsRepository(client)

service = SheetsService(repo, DataTransformer())


sheets_service = service.get_normalized_data(range_name=RANGE_NAME)


# @afiliados_bp.route("/sync", methods=["POST"])
# def sync_afiliados():
#     # 1️⃣ Obtener datos normalizados
#     data = sheets_service

#     # 2️⃣ Convertir a modelos SQLAlchemy
#     # afiliados_instances = []
#     # for row in data:
#     #     #afiliado = Afiliado()
#     #     #afiliados_instances.append(afiliado)

#     #     # Si tiene cónyuge
#     #     if row.get("conyuge"):
#     #         conyuge = Conyuge(
#     #             nombre_apellido=row["conyuge"]["nombre_apellido"],
#     #             dni=row["conyuge"]["dni"],
#     #             afiliado_id=None  # asignar después si necesitas
#     #         )
#     #         db.session.add(conyuge)

#     # # 3️⃣ Guardar en la base de datos
#     # db.session.add_all(afiliados_instances)
#     # db.session.commit()

#     return jsonify({"status": "ok", "total_afiliados": len(data)}), 200
@afiliados_bp.route("/sync", methods=["GET"])
def sync_afiliados():
    
    return jsonify({
        "status": "ok",
        "total": len(sheets_service),
        "data": sheets_service,
        "message": "Datos sincronizados correctamente"
        
    }), 200