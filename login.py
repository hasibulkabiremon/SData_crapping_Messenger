from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle
import os
from dotenv import load_dotenv

load_dotenv()
class MessengerBotLogin:
    def __init__(self, username, password, cookies_path="messenger_cookies.pkl"):
        self.username = username
        self.password = password
        self.cookies_path = cookies_path
        self.driver = self._initialize_webdriver()

    def _initialize_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", False)
        return webdriver.Chrome(options=options)

    def load_cookies(self):
        try:
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print("Cookies loaded successfully.")
        except FileNotFoundError:
            print("Cookies file not found.")

    def save_cookies(self):
        with open(self.cookies_path, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        print(f"Cookies saved to {self.cookies_path}")

    def login_manually(self):
        username_input = self.driver.find_element(By.XPATH, '//input[@id="email"]')
        password_input = self.driver.find_element(By.XPATH, '//input[@id="pass"]')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

    def login_with_cookies(self):
        self.driver.get("https://www.facebook.com/")
        time.sleep(5)

        self.load_cookies()
        self.driver.refresh()
        time.sleep(5)

    def run(self):
        try:
            self.driver.get("https://www.facebook.com/messages/t/29059462703645005")
            time.sleep(5)

            self.load_cookies()
            self.driver.refresh()
            time.sleep(5)

            if not self.is_logged_in():
                print("Logging in manually...")
                self.login_manually()
                self.save_cookies()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            None
            # self.driver.quit()

    def is_logged_in(self):
        try:
            self.driver.find_element(By.XPATH, '//input[@placeholder="Search Facebook"]')
            return True
        except Exception:
            return False
    # ... existing code ...

    def get_messages(self, num_messages=10):
        """
        Retrieves messages from the current Messenger conversation
        
        Args:
            num_messages: Number of messages to retrieve (default: 10)
        
        Returns:
            list: List of dictionaries containing message data
        """
        messages = []

        message_container_xpath = os.getenv("MESSAGE_CONTAINER_XPATH")
        print(message_container_xpath)
        try:
            # Wait for messages to load
            message_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, message_container_xpath))
            ) 
            # message_elements = self.driver.find_elements(By.XPATH, os.getenv("MESSAGE_CONTAINER_XPATH"))
            print(len(message_elements))
            print(message_elements)
        
            # Process the most recent messages (up to num_messages)
            for idx, element in enumerate(message_elements):
                try:
                    try:
                        # Get message text - updated selector for Facebook Messenger
                        message_text = self.driver.find_element(By.XPATH, f'({os.getenv("MESSAGE_CONTAINER_XPATH")})[{idx + 1}]{os.getenv("MESSAGE_XPATH")}').text
                    except:
                        try:
                            message_text = self.driver.find_element(By.XPATH, f'({os.getenv("MESSAGE_CONTAINER_XPATH")})[{idx + 1}]{os.getenv("MESSAGE_XPATH2")}').text
                        except: 
                            message_text = "Unknown"
                            continue
                    
                    # Get sender name (if available)
                    try:
                        sender = self.driver.find_element(By.XPATH, f'({os.getenv("MESSAGE_CONTAINER_XPATH")})[{idx + 1}]{os.getenv("SENDER_XPATH")}').text
                    
                    except Exception as e:
                        try:
                            sender = self.driver.find_element(By.XPATH, f'({os.getenv("MESSAGE_CONTAINER_XPATH")})[{idx + 1}]{os.getenv("SENDER_XPATH2")}').text
                        except Exception as e2:
                            print(f"Error getting sender: {e}")
                            print(f"Error getting sender2: {e2}")
                            sender = "Unknown"
                    
                    # Get timestamp (if available)
                    try:
                        timestamp = self.driver.find_element(By.XPATH, f'({os.getenv("MESSAGE_CONTAINER_XPATH")})[{idx + 1}]{os.getenv("MESSAGE_TIME")}').text
                    except Exception as e:
                        print(f"Error getting timestamp: {e}")
                        timestamp = "Unknown"
                    
                    messages.append({
                        'sender': sender,
                        'text': message_text,
                        'timestamp': timestamp
                    })
                    
                except Exception as e:
                    print(f"Error processing message {idx}: {str(e)}")
                    continue
                    
            print(f"Successfully retrieved {len(messages)} messages")
            return messages
            
        except TimeoutException:
            print("Failed to load messages - timeout")
            return messages
        except Exception as e:
            print(f"An error occurred while getting messages: {str(e)}")
            return messages

# ... existing code ...

if __name__ == "__main__":
    username = "01730805675"
    password = "Test@1234"

    bot = MessengerBotLogin(username, password)
    bot.run()
