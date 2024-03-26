from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION = os.getenv('SESSION')
REDIRECT_TO = os.getenv('REDIRECT_TO')
FROM_USER_ID = int(os.getenv('FROM_USER_ID'))
FROM_CHAT_ID = os.getenv('FROM_CHAT_ID')

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


@client.on(events.NewMessage(incoming=True, chats=[FROM_CHAT_ID], from_users=FROM_USER_ID))
async def my_event_handler(event):
    try:
        message = event.raw_text
        is_reply = event.is_reply
        reply_message = 'none'
        user_id = event.message.from_id.user_id

        if is_reply:
            reply_message = await event.get_reply_message()

        channel = await client.get_entity(REDIRECT_TO)
        await client.send_message(entity=channel, message=f"**{message}** reply to => *{reply_message.text}*")

        logger.info(f"message: {message}, isReply:{is_reply}, reply:{reply_message.text}, user_id: {user_id}, date: {event.date}")

    except (BrokenPipeError, IOError) as error:
        logger.error(f"[TelegramClientListener] {type(error).__name__}: {error}")

logger.info("Start listening new messages")
client.start()
client.run_until_disconnected()
