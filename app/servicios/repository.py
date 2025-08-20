from .sheets_client import ISheetsClient

# 3. Repositorio

class GoogleSheetsRepository:

    def __init__(self, client: ISheetsClient):
        self.client = client
    
    def get_raw_data(self, range_name):
        return self.client.read_range(range_name)