import os

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from datetime import datetime

from ..servicios.sheets_service import SheetsService
from ..servicios.repository import GoogleSheetsRepository
from ..servicios.transformer import DataTransformer
from ..servicios.sheets_client import GoogleSheetsClient
from ..servicios.afiliado_service import FactoryAfiliado

from .. import db
# Schemas y modelos
from ..models.modelo_afiliado import Afiliado, AfiliadoSchema
from ..models.modelo_conyuge import Conyuge, ConyugeSchema
from ..models.modelo_hijo import Hijo, HijoSchema
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


factory = FactoryAfiliado()


@afiliados_bp.route("/factory", methods=["GET"])
def crear_afiliado_completo():
    try:
        # Validar método POST tendria que ser
        if request.method != 'GET':
            return jsonify({
                "status": "error",
                "message": "Método no permitido"
            }), 405
        
        resultados = []
        exitosos = 0
        fallidos = 0
        
        # Procesar cada sheet service
        for i in range(len(sheets_service)):
            try:
                data = sheets_service[i]
                
                # Validar datos básicos
                if not data or not isinstance(data, dict):
                    raise ValueError("Datos inválidos o vacíos")
                
                result = factory.crear_afiliado_completo(data)
                
                if result["status"] == "ok":
                    exitosos += 1
                    resultados.append({
                        "sheet_index": i,
                        "status": "success",
                        "message": "Afiliado creado exitosamente",
                        "data": result.get("data", {})
                    })
                else:
                    fallidos += 1
                    resultados.append({
                        "sheet_index": i,
                        "status": "error",
                        "message": result.get("message", "Error al crear afiliado"),
                        "error": result.get("error")
                    })
                    
            except Exception as e:
                fallidos += 1
                resultados.append({
                    "sheet_index": i,
                    "status": "error",
                    "message": f"Error procesando sheet {i}",
                    "error": str(e)
                })
        
        # Respuesta final
        if exitosos > 0:
            return jsonify({
                "status": "success",
                "message": f"Carga completada. {exitosos} afiliados creados, {fallidos} fallos",
                "total": len(sheets_service),
                "exitosos": exitosos,
                "fallidos": fallidos,
                "detalles": resultados
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "No se pudo crear ningún afiliado",
                "total": len(sheets_service),
                "fallidos": fallidos,
                "errores": resultados
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error interno del servidor",
            "error": str(e)
        }), 500


@afiliados_bp.route("/lista_afiliados", methods=["GET"])
def listar_afiliados():
    try:
        schema_afiliado = AfiliadoSchema(many=True)
        listar_afiliados = Afiliado.query.all()
        
        # Respuesta estructurada correctamente
        return jsonify({
            "status": "success",
            "message": "Afiliados obtenidos exitosamente",
            "data": schema_afiliado.dump(listar_afiliados),
            "meta": {
                "total": len(listar_afiliados),
                "timestamp": datetime.now().isoformat()
            }
        }), 200  # Código HTTP explícito
        
    except Exception as e:
        # Manejo de errores
        return jsonify({
            "status": "error",
            "message": "Error al obtener los afiliados",
            "error": str(e)
        }), 500
    

@afiliados_bp.route("/afiliado/<int:id>", methods=["GET"])
def obtener_afiliado(id):
    try:
        # Validar que el ID sea positivo
        if id <= 0:
            return jsonify({
                "status": "error",
                "message": "ID debe ser un número positivo",
                "code": "INVALID_ID"
            }), 400
        
        # Buscar el afiliado
        afiliado = Afiliado.query.get(id)
        
        if not afiliado:
            return jsonify({
                "status": "error",
                "message": f"Afiliado con ID {id} no existe",
                "code": "AFILIADO_NOT_FOUND",
                "suggestions": [
                    "Verifique el ID proporcionado",
                    "Consulte la lista de afiliados disponibles"
                ]
            }), 404
        
        schema = AfiliadoSchema()
        
        return jsonify({
            "status": "success",
            "message": "Afiliado encontrado exitosamente",
            "data": schema.dump(afiliado),
            "meta": {
                "resource_id": id,
                "timestamp": datetime.now().isoformat(),
                "resource_type": "afiliado"
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error al procesar la solicitud",
            "code": "INTERNAL_SERVER_ERROR",
            "error": str(e)
        }), 500