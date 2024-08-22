import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from loguru import logger
import telegram
import asyncio
import json
from webdriver_manager.chrome import ChromeDriverManager

# create a telegram bot instance
bot = telegram.Bot(token="use BotFather to create bot and paste token here")


async def send_message(text, chat_id="chat ID to where the message will be sent. (conversation or group)"):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


# defining the User-Agent header to use in the GET request below
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# Define multiple wallet URLs
wallet_urls = [
    "https://www.pump.fun/profile/",
    "https://www.pump.fun/profile/",
    "https://www.pump.fun/profile/",
    # Add more wallet URLs as needed
]

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
