import requests
import os
import mimetypes


class WhatsappAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://graph.facebook.com/v20.0/'

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',

        }

    def get(self, endpoint):
        headers = self._get_headers()
        res = requests.get(self.base_url + endpoint, headers=headers)
        print(self.base_url + endpoint)
        return res.json()

    def post(self, endpoint, data, files=None):
        headers = self._get_headers()
        res = requests.post(self.base_url + endpoint, headers=headers, json=data, files=files)
        return res.json()

    def upload_media(self, phone_number_id, file_path):
        # Obtener el nombre del archivo y el tipo MIME automáticamente
        file_name = os.path.basename(file_path)  # Extrae solo el nombre del archivo
        mime_type, _ = mimetypes.guess_type(file_path)  # Detecta el tipo MIME basado en la extensión del archivo
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Tipo genérico para archivos binarios

        # Estructura de files con nombre de archivo y tipo MIME detectados
        files = [
            ("file", (file_name, open(file_path, 'rb'), mime_type))
        ]

        data = {
            'messaging_product': 'whatsapp',
        }

        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        try:
            res = requests.post(self.base_url + f'/{phone_number_id}/media', headers=headers, data=data, files=files)
            return res.json()

        except Exception as error:
            print("Error", error, type(error).__name__)
            return error

    def send_message(self, phone_number_id, body=None):
        if body is None:
            body = {}

        try:
            response = self.post(f'/{phone_number_id}/messages', body)
            return response
        except Exception as error:
            print("Error", error, type(error).__name__)
            return error
