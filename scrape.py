from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import pytz
from email_utils import send_email
from send_message import send_message

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION = os.getenv('SESSION')
FROM_CHAT_ID = os.getenv('FROM_CHAT_ID')
FROM_USERNAME = os.getenv('FROM_USERNAME')
SUBJECT = os.getenv('SUBJECT')
SENDER = os.getenv('SENDER')
PASSWORD = os.getenv('PASSWORD')
RECIPIENTS = os.getenv('RECIPIENTS')

log_file = 'app.log'

handler = None
if os.getenv("ENVIRONMENT") == "production":
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    handler.suffix = '%d-%m-%Y'
else:
    handler = logging.StreamHandler()  # Log a la consola en desarrollo
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

client = TelegramClient(
    session=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    auto_reconnect=True,
    sequential_updates=True,
    retry_delay=0,
    flood_sleep_threshold=0,
)


async def my_event_handler(event):
    try:
        msg = event.raw_text
        username = event.message.sender.first_name
        date = event.date

        desired_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
        formatted_date = date.astimezone(desired_timezone).strftime("%d-%m %H:%M")

        saved_path = None
        if event.photo:
            saved_path = await event.download_media()

        # is_reply = event.is_reply
        # reply_message = 'none'
        # if is_reply:
        #    reply_message = await event.get_reply_message()

        # send_email(SUBJECT, SENDER, [RECIPIENTS], PASSWORD, msg, formatted_date, username, saved_path)
        send_message(msg, formatted_date, saved_path)
        if saved_path:
            os.remove(saved_path)

        logger.info(f"User: {username}, path: {saved_path}, date: {formatted_date}")

    except (BrokenPipeError, IOError) as error:
        logger.error(f"[Send Email] {type(error).__name__}: {error}")


@client.on(events.NewMessage(incoming=True, chats=[FROM_CHAT_ID]))
async def message_listener(event):
    if hasattr(event.message, 'sender') and hasattr(event.message.sender,
                                                    'first_name') and event.message.sender.first_name == FROM_USERNAME:
        await my_event_handler(event)


logger.info("Start listening new messages")
client.start()
client.run_until_disconnected()
