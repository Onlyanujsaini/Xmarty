import subprocess
import time
import logging
from aiogram import Bot
import asyncio

API_TOKEN = '7543592031:AAHnlEqSQg2MC_Dimz8Hi71iMD8GfYrweTM'
ADMIN_ID = '6704542925'
MAX_RESTARTS = 50
RESTART_PERIOD = 5  # Seconds

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
bot = Bot(API_TOKEN)

async def start_bot():
    """Start the bot script as a subprocess."""
    process = await asyncio.create_subprocess_exec('python3', 'm.py')
    return process

async def notify_admin(message):
    """Send a notification message to the admin via Telegram."""
    try:
        await bot.send_message(ADMIN_ID, message)
        logging.info("Admin notified: %s", message)
    except Exception as e:
        logging.error("Failed to send message to admin: %s", e)

async def main():
    """Main function to manage bot process lifecycle."""
    restart_count = 0
    last_restart_time = time.time()

    while True:
        if restart_count >= MAX_RESTARTS:
            current_time = time.time()
            if current_time - last_restart_time < RESTART_PERIOD:
                wait_time = RESTART_PERIOD - (current_time - last_restart_time)
                logging.warning("Maximum restart limit reached. Waiting for %.2f seconds...", wait_time)
                await notify_admin(f"⚠️ Maximum restart limit reached. Waiting for {int(wait_time)} seconds before retrying.")
                await asyncio.sleep(wait_time)
            restart_count = 0
            last_restart_time = time.time()

        logging.info("Starting the bot...")
        process = await start_bot()
        await notify_admin("🚀 Bot is starting...")

        while True:
            return_code = await process.wait()
            if return_code is None:
                await asyncio.sleep(5)
            else:
                break

        logging.warning("Bot process terminated. Restarting in 10 seconds...")
        await notify_admin("⚠️ The bot has crashed and will be restarted in 10 seconds.")
        restart_count += 1
        await asyncio.sleep(10)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Nand script terminated by user.")
