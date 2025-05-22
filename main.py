import time
from login import MessengerBotLogin
import os
from dotenv import load_dotenv
import json
load_dotenv()

username = os.getenv("USERNAME")    
password = os.getenv("PASSWORD")

bot = MessengerBotLogin(username, password)
bot.run()

# Create source.json with URLs

# Load URLs from source.json
with open('source.json', 'r', encoding='utf-8') as source_file:
    urls = json.load(source_file)


# Iterate over each URL and retrieve messages
for url in urls:
    bot.driver.get(url)  # Navigate to the URL
    time.sleep(10)
    messages_data = []
    bot.get_messages(messages_data)

    # Sort the messages_data list by the 'timestamp' key
    from datetime import datetime

    # Convert the timestamp string to a datetime object for accurate sorting
    messages_data.sort(key=lambda message: datetime.strptime(message['timestamp'], "%Y-%m-%d %H:%M:%S"))
    # Convert the URL to a valid filename by replacing special characters
    url_filename = url.replace("https://", "").replace("/", "_").replace(":", "_") + ".json"
    
    # Write the messages data to a JSON file named after the URL
    with open(f'post_data/{url_filename}', 'w', encoding='utf-8') as url_json_file:
        json.dump(messages_data, url_json_file, indent=4, ensure_ascii=False)
    
