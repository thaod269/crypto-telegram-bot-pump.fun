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

# Create a telegram bot instance
bot = telegram.Bot(token="YOUR_TELEGRAM_BOT_TOKEN")

async def send_message(text, chat_id="YOUR_TELEGRAM_CHAT_ID"):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

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
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

# Create a Chrome webdriver instance using webdriver_manager to manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

async def main():
    while True:
        for base_url in wallet_urls:
            logger.info(f"Loading the page for wallet: {base_url}")
            driver.get(base_url)
            driver.refresh()
            time.sleep(4)  # Waiting to allow data to load
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            target_divs = soup.find_all("div", class_="grid gap-4 text-sm min-w-[350px] w-fit")
            data_array = []

            for div in target_divs:
                amount_ticker_div = div.find("div").find("div")
                amount = amount_ticker_div.text.split(" ")[0]
                ticker = amount_ticker_div.text.split(" ")[1]
                link = div.find("a")["href"]
                value = amount_ticker_div.find_next_sibling("div").text
                if value != "0.0000 SOL":
                    data_object = {
                        "TICKER": ticker,
                        "VALUE": value,
                        "AMOUNT": amount,
                        "LINK": "https://www.pump.fun" + link,
                    }
                    data_array.append(data_object)

            if not data_array:
                logger.error("No data found")
                continue

            # Filename based on wallet address for uniqueness
            output_filename = f"output_{base_url.split('/')[-1]}.json"
            try:
                with open(output_filename, "r") as f:
                    previous_tickers = json.load(f)
            except FileNotFoundError:
                previous_tickers = []

            new_tickers = [data for data in data_array if data["TICKER"] not in previous_tickers]
            if new_tickers:
                new_tickers_message = "New Tickers:\n"
                for new_ticker in new_tickers:
                    new_tickers_message += (f"Ticker: {new_ticker['TICKER']}\n"
                                            f"Amount: {new_ticker['AMOUNT']}\n"
                                            f"Value: {new_ticker['VALUE']}\n"
                                            f"Link: {new_ticker['LINK']}\n\nProfile: {base_url}\n\n")
                await send_message(new_tickers_message)
                logger.info(new_tickers_message)
            else:
                logger.info("No new tickers found")

            with open(output_filename, "w") as f:
                json.dump([data["TICKER"] for data in data_array], f)

            time.sleep(1)  # Wait before the next check

# Running the main function
asyncio.run(main())
