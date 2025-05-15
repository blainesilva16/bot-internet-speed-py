from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time,os,dotenv

dotenv.load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.up = 0
        self.down = 0
        # self.up = 23.81
        # self.down = 28.16

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(15)
        try:
            go = self.driver.find_element(By.CSS_SELECTOR, '.start-button a')
        except:
            print("Button not found")
        else:
            go.click()

        time.sleep(90)

        try:
            download = self.driver.find_element(By.CLASS_NAME, 'download-speed').text
            upload = self.driver.find_element(By.CLASS_NAME, 'upload-speed').text
        except:
            print("Value(s) not found")
        else:
            self.down = float(download)
            self.up = float(upload)
            print("Download speed:",self.down)
            print("Upload speed:", self.up)

    def tweet_at_provider(self):
        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            self.driver.get("https://x.com/i/flow/login")
            time.sleep(60)
            # Logging in
            try:
                # Searching for email input
                input = self.driver.find_element(By.NAME, 'text')
            except NoSuchElementException:
                print("Element for email not found.")
            else:
                input.send_keys(TWITTER_EMAIL,Keys.ENTER)
            time.sleep(20)
            try:
                # Searchin for password input
                pass_input = self.driver.find_element(By.NAME, 'password')
            except NoSuchElementException:
                print("Element for password not found.")
            else:
                pass_input.send_keys(TWITTER_PASSWORD,Keys.ENTER)
            # Locate the tweet box and prepare message
            time.sleep(10)
            try:
                posting_input = self.driver.find_element(By.XPATH,
                                                     value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div')
            except NoSuchElementException:
                print("Element for writing tweet not found.")
            else:
                # Message to tweet
                message = (
                    f"Hey Internet Provider @, why is my internet speed "
                    f"{self.down} down/{self.up} up when I pay for {PROMISED_DOWN} down/{PROMISED_UP}up?"
                )

                # Click and write the message
                posting_input.click()
                posting_input.send_keys(message)
            time.sleep(15)

            # Click the "Tweet" button to post
            try:
                post_btn = self.driver.find_element(By.CSS_SELECTOR, value='button[data-testid="tweetButtonInline"]')
            except NoSuchElementException:
                print("Element for twitting not found.")
            else:
                post_btn.click()
            print(f"Hey Internet Provider @, why is my internet speed "
                    f"{self.down} down/{self.up} up when I pay for {PROMISED_DOWN} down/{PROMISED_UP}up?"
                )
        else:
            print("Your internet is working as expected.")
        # self.driver.quit()

