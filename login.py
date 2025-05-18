from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle
import os
from dotenv import load_dotenv

from timestamp_converter import standardize_timestamp

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
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(2)  # Set implicit wait on the driver instance
        return driver

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
            self.driver.get("https://www.facebook.com/")
            # time.sleep(5)
            
            try:
                self.load_cookies()
                self.driver.refresh()
                # time.sleep(5)
            except:
                pass

            if not self.is_logged_in():
                self.login_manually()
                self.save_cookies()

        except Exception as e:
            import traceback
            print(f"An error occurred: {e}")
            traceback.print_exc()

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

    def highlight(self, element, duration=1, color="red", border="2px"):
        """Highlights (blinks) a Selenium WebDriver element"""
        driver = self.driver  # Use the class's driver instance
        original_style = element.get_attribute('style')
        new_style = f"border: {border} solid {color}; {original_style}"
        driver.execute_script(f"arguments[0].setAttribute('style', '{new_style}')", element)
        time.sleep(duration)
        driver.execute_script(f"arguments[0].setAttribute('style', '{original_style}')", element)


    def get_messages(self, messages_data):
        """
        Retrieves messages from the current Messenger conversation
        
        Args:
            num_messages: Number of messages to retrieve (default: 10)
        
        Returns:
            list: List of dictionaries containing message data
        """

        message_container_xpath = os.getenv("MESSAGE_CONTAINER_XPATH")
        print(message_container_xpath)
        seen_messages = set()
        for attempt in range(10):
            end_time = time.time() + 1 # 10 seconds from now
            while time.time() < end_time:
                found = False
                try:
                    loading_element = self.driver.find_element(By.XPATH, os.getenv("LOADING_XPATH"))
                    loading_element.click()
                    end_time = time.time() + 1 # 2 additional seconds
                    found = True
                    print("->->->->->->->->->->Loading found and clicked->->->->->->->->->->")
                except:
                    if found:
                        break


            print("Attempt:", attempt)
            if "message_elements" in locals() and len(message_elements) > 0:
                # input("message_elements")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", message_elements[0])
            try:
                # Wait for messages to load
                new_message_elements = self.driver.find_elements(By.XPATH, os.getenv("MESSAGE_CONTAINER_XPATH"))
                message_elements = [element for element in new_message_elements if element not in seen_messages]
                seen_messages.update(message_elements)
                print(f"Found {len(message_elements)} new message elements")
                
                # Create a set to track unique messages
                
                
                # Process the most recent messages
                self.driver.implicitly_wait(0)
                for element in reversed(message_elements):
                    
                    print("element:", message_elements.index(element))
                    try:
                        # Get message text
                        try:
                            message_text_element = element.find_element(By.XPATH, os.getenv("MESSAGE_XPATH"))
                            message_text = message_text_element.text
                            try:
                                self.highlight(message_text_element)  # Ensure 'highlight' is called as a method of the class
                            except Exception as e:
                                print(f"Error highlighting message text element: {e}")
                                pass
                            
                        except:
                            try:
                                message_text_element = element.find_element(By.XPATH, os.getenv("MESSAGE_XPATH2"))
                                message_text = message_text_element.text
                                try:
                                    self.highlight(message_text_element)  # Ensure 'highlight' is called as a method of the class
                                except Exception as e:
                                    print(f"Error highlighting message text element: {e}")
                                    message_text = "Not found"
                                    pass
                                sender = "You"
                            except:
                                message_text = "Not found"
                                sender = "Unknown"

                            
                                # continue
                        finally:
                            print("message_text:", message_text)
                        
                        # Skip if we've seen this message before

                        try:
                            user_profile_pic_element = element.find_element(By.XPATH, os.getenv("USER_PROFILE_PIC_XPATH"))
                            self.highlight(user_profile_pic_element)
                            user_profile_pic = user_profile_pic_element.get_attribute("src")
                            if sender == "Unknown":
                                try:    
                                    sender = user_profile_pic_element.get_attribute("alt")
                                except:
                                    sender = "Unknown"
                        except:
                            user_profile_pic = "Not found"
                        
                        try:
                            media_element = element.find_element(By.XPATH, os.getenv("IMAGE_PATH"))
                            self.highlight(media_element)
                            media = media_element.get_attribute("src")
                            
                            if message_text == "Not found":
                                try:
                                    message_text = media_element.get_attribute("alt")
                                except:
                                    pass
                        except: 
                            media = "Not found"
                        
                        # Get sender name
                        if sender == "Unknown":
                            try:
                                sender = element.find_element(By.XPATH, os.getenv("SENDER_XPATH"))
                                self.highlight(sender)
                                sender = sender.text
                            except Exception as e:
                                print("User Exceptions SENDER_XPATH:")
                                try:
                                    sender = element.find_element(By.XPATH, os.getenv("SENDER_XPATH2"))
                                    self.highlight(sender)
                                    sender = sender.text
                                except Exception as e2:
                                    print("User Exceptions SENDER_XPATH2:")
                                    sender = "Unknown"
                            finally:
                                print("sender:", sender)
                        
                        # Get timestamp
                        try:
                            ActionChains(self.driver).move_to_element(message_text_element).perform()
                            tooltip_text = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, os.getenv("TOOLTIP_XPATH")))
                            )
                            self.highlight(tooltip_text)
                            timestamp = standardize_timestamp(tooltip_text.text)
                            print("timestamp:", timestamp)
                        except Exception as e:
                            timestamp = "Unknown"

                        # message_identifier = (message_text, sender, timestamp)
                        # if message_identifier in seen_messages:
                        #     print("Message already seen:", message_identifier)
                        #     continue
                        # seen_messages.add(message_identifier)
                        
                        messages_data.append({
                            'user_name': sender,
                            'user_profile_pic': user_profile_pic,
                            'text': message_text,
                            'media': media,
                            'timestamp': timestamp
                        })
                        
                    except Exception as e:
                        print(f"Error processing message: {str(e)}")
                        continue
                        
                print(f"Successfully retrieved {len(messages_data)} unique messages")
                # break  # Exit the loop if successful

            except TimeoutException:
                print("Failed to load messages - timeout")
                
            except Exception as e:
                print(f"An error occurred while getting messages: {str(e)}")


            

# ... existing code ...

# if __name__ == "__main__":
#     username = "01730805675"
#     password = "Test@1234"

#     bot = MessengerBotLogin(username, password)
#     bot.run()
