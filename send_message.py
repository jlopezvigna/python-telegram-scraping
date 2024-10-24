import sys
import os
import json


current_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from dotenv import load_dotenv
from whatsapp import WhatsappAPI

load_dotenv()

SUBJECT = os.getenv('SUBJECT')
WP_TOKEN = os.getenv('WP_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
PHONE_DESTINATARI = os.getenv('PHONE_DESTINATARI')

wp = WhatsappAPI(WP_TOKEN)

ALERT_MESSAGE = 'alert_messsage'
ALERT_MESSAGE_WITH_IMAGE = 'alert_messsage_with_image'


def send_message(text, date, file_path=None):
    media_id = None
    try:
        template_name = ALERT_MESSAGE
        if file_path:
            template_name = ALERT_MESSAGE_WITH_IMAGE
            response = wp.upload_media(PHONE_NUMBER_ID, file_path)
            media_id = response.get("id")
            if response.get("error"):
                print(f"Upload Media Failed - {response['error']}")
                return

        # Cargar el JSON base
        wp_template_dir = os.path.join(root_dir, "templates/wp_base.json")

        with open(wp_template_dir, 'r') as json_file:
            base_data = json.load(json_file)

        # Modificar dependiendo de las variables
        base_data["to"] = PHONE_DESTINATARI
        base_data["template"]["name"] = template_name
        base_data["template"]["components"][0]["parameters"][0]["text"] = text
        base_data["template"]["components"][0]["parameters"][1]["date_time"]["fallback_value"] = date

        if template_name == ALERT_MESSAGE_WITH_IMAGE:
            base_data["template"]["components"].append(
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "id": media_id,
                            }
                        }
                    ]
                }
            )

        res = wp.send_message(PHONE_NUMBER_ID, base_data)
        if res.get("error"):
            print(f"Send Message Failed - {res['error']}")
        else:
            message_id = res['messages'][0]['id']
            print(f"Send Message Success || {message_id}")

    except (BrokenPipeError, IOError) as error:
        print(f"Command Failed - {type(error).__name__}: {error}")
