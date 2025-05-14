from login import MessengerBotLogin
import os
from dotenv import load_dotenv
import json
load_dotenv()

username = os.getenv("USERNAME")    
password = os.getenv("PASSWORD")

bot = MessengerBotLogin(username, password)
bot.run()

messages_data = []
bot.get_messages(messages_data)

# Get last 5 messages
# Write the last five messages to a JSON file
with open('post_data/messages.json', 'w',encoding='utf-8') as json_file:
    json.dump(messages_data, json_file, indent=4,ensure_ascii=False)
