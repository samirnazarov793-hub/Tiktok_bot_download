import telebot
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = "8514900140:AAH5sPY72csZXq-0Mvjv1TZM0R9gmkaiXRY"
bot = telebot.TeleBot(TOKEN)

user_last_message = {}
SPAM_LIMIT = 2


@bot.message_handler(content_types=['text', 'sticker', 'animation', 'photo', 'video', 'document'])
def check_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    if user_id in user_last_message:
        if current_time - user_last_message[user_id] < SPAM_LIMIT:
            if message.content_type in ["sticker", "animation"]:
                try:
                    bot.delete_message(chat_id, message.message_id)
                except Exception as e:
                    logger.warning(f"Could not delete message: {e}")
            return

    user_last_message[user_id] = current_time


if name == "__main__":
    logger.info("Bot started. Polling for updates...")
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 409:
                logger.error("Conflict: another bot instance is running. Retrying in 30 seconds...")
                time.sleep(30)
            else:
                logger.error(f"Telegram API error: {e}")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(5)