from .repository import GoogleSheetsRepository
from .transformer import DataTransformer

# 5. Coordinador (antes FactoryGoogleSheetsService)
class SheetsService:
    """
    Servicio para interactuar con Google Sheets, utilizando un repositorio y un transformador de datos
    """
    def __init__(self, repo: GoogleSheetsRepository, transformer: DataTransformer):
        self.repo = repo
        self.transformer = transformer

    def get_normalized_data(self, range_name):
        raw = self.repo.get_raw_data(range_name)
        normalized_rows = self.transformer.normalize_empty(raw_data=raw, num_columns=len(raw[0]))
        # Convertir las filas normalizadas a diccionarios usando los encabezados
        dicts = self.transformer.to_dicts(raw_data=normalized_rows[1:], headers=raw[0])
        return self.transformer.normalize_input(dicts=dicts)
