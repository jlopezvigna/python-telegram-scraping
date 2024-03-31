from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from email_utils import send_email

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION = os.getenv('SESSION')
FROM_CHAT_ID = os.getenv('FROM_CHAT_ID')
FROM_USERNAME = int(os.getenv('FROM_USERNAME'))
SUBJECT = os.getenv('SUBJECT')
SENDER = os.getenv('SENDER')
PASSWORD = os.getenv('PASSWORD')
RECIPIENTS = os.getenv('RECIPIENTS')

log_file = 'app.log'
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
handler.suffix = '%Y-%m-%d'
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
        is_reply = event.is_reply

        # reply_message = 'none'
        # if is_reply:
        #    reply_message = await event.get_reply_message()

        send_email(SUBJECT, SENDER, [RECIPIENTS], PASSWORD, msg, date, username)

        logger.info(f"message: {msg}, isReply:{is_reply}, username: {username}, date: {date}")

    except (BrokenPipeError, IOError) as error:
        logger.error(f"[TelegramClientListener] {type(error).__name__}: {error}")


@client.on(events.NewMessage(incoming=True, chats=[FROM_CHAT_ID]))
async def message_listener(event):
    if event.message.sender.first_name == FROM_USERNAME:
        await my_event_handler(event)


logger.info("Start listening new messages")
client.start()
client.run_until_disconnected()
