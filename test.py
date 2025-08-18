from app.servicios.google_sheets_service import FactoryGoogleSheetsService


lista_afiliados = FactoryGoogleSheetsService().normalizer_list()

if __name__ == "__main__":
    print("Cargar datos normalizados a la base de datos:")
    print(lista_afiliados[0])  # Imprimir el primer afiliado normalizado
    