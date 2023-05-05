import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
from re import sub
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
}

url = 'https://www.microsoft.com/de-de/store/collections/xboxconsoles'
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
device = 0

conn = sqlite3.connect('prices.db')
c = conn.cursor()

# Create a table to store the prices
c.execute('''CREATE TABLE IF NOT EXISTS prices
             (xbox_pid TEXT PRIMARY KEY,
              name TEXT,
              price INTEGER,
              date TEXT)''')

def send_telegram_message(bot_token, chat_id, message):
    if bot_token is not None and chat_id is not None:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        requests.post(url, data=data)

elements = soup.findAll(attrs={'data-bi-pid': True})
for xbox_element in elements:
    xbox_pid= xbox_element.get('data-bi-pid')
    xbox_name = xbox_element.get('data-bi-prdname')

    with open(str(device)+'.html', 'w', encoding='utf-8') as file:
        file.write(xbox_element.text)

    price_element = xbox_element.find('p', {'class': 'sr-only'})

    if xbox_name is not None and price_element is not None:
        xbox_price = int(sub(r'[^\d]', '', price_element.text.strip()))

        # Check if the price has changed
        c.execute('SELECT price FROM prices WHERE xbox_pid = ? ORDER BY date DESC LIMIT 1', (xbox_pid,))
        last_price = c.fetchone()
        if last_price is not None and last_price[0] != xbox_price:
            message = f'Price for {xbox_name} has changed from {last_price[0]/100:.2f} to {xbox_price/100:.2f}'
            send_telegram_message(bot_token, chat_id, message)
            print(message)
        else:
            print(f'Price for {xbox_name} is {xbox_price/100:.2f}')

        # Insert the new price into the database
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT OR REPLACE INTO prices (xbox_pid, name, price, date) VALUES (?, ?, ?, ?)', (xbox_pid, xbox_name, xbox_price, date))
        conn.commit()

conn.close()
