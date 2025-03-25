from login import MessengerBotLogin
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("USERNAME")    
password = os.getenv("PASSWORD")

bot = MessengerBotLogin(username, password)
bot.run()

messages = bot.get_messages(num_messages=5)  # Get last 5 messages
for msg in messages:
    print(f"{msg['sender']} ({msg['timestamp']}): {msg['text']}")