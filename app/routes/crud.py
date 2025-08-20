from flask import Blueprint, render_template, redirect, url_for, flash, request
#from ..servicios.google_sheets_service import FactoryGoogleSheetsService

# asignar un nombre al blueprint
crud = Blueprint('crud', __name__)

@crud.route('/afiliados' , methods=['GET'])
def listar_afiliados():
    # Lógica para listar afiliados
    pass
    
    return render_template('afiliados/listar.html')

@crud.route('/create/afiliado', methods=['POST'])
def crear_afiliado():
    # Lógica para crear un nuevo afiliado
    return render_template('afiliados/crear.html')

@crud.route('/afiliado/<string:id>', methods=['GET','POST'])
def obtener_afiliado(id):
    # Lógica para obtener un afiliado por ID
    return render_template('afiliados/detalles.html', id=id)

@crud.route('/update/afiliado/<string:id>', methods=['GET']) #metodo put 
def actualizar_afiliado(id):
    # Lógica para actualizar un afiliado por ID
    return render_template('afiliados/editar.html', id=id)

@crud.route('/delete/afiliado/<string:id>', methods=['GET']) # metodo delete
def eliminar_afiliado(id):
    # Lógica para eliminar un afiliado por ID
    return render_template('afiliados/eliminar.html', id=id)
