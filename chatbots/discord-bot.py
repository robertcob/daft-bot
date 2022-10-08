import os
import discord.ext
from discord.ui import Button, View
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    print("activated")
    print(message.content)
    if message.content.startswith('NEW PROPERTY!'):
        rawLink = message.split("\n")[3]
        url = rawLink.split(' ')[4]
        print("PROPERTY URL -> " + url)
        button = Button(label="Apply to property?", style=discord.ButtonStyle.blurple, emoji="🏠")
        async def button_callback(interaction):
            interaction.response.defer()
            success = send_message(url)
            if success:
                print("function ran successfully")
                interaction.edit_original_message("email sent successfully!", view=None)
            else:
                interaction.edit_original_message("email failed to send!")
                button.style = discord.ButtonStyle.red

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await message.channel.send("Click to apply", view=view)

def send_message(propertyURL):
    success = False
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    authURL = "https://www.daft.ie/auth/authenticate"
    driver.get(authURL)
    driver.find_element(By.XPATH, value='''//*[@id="username"]''').send_keys(os.environ['DAFTEMAIL'])
    password = driver.find_element(By.XPATH, value='''//*[@id="password"]''')
    password.send_keys(os.environ['DAFTPASSWORD'])
    password.send_keys(Keys.ENTER)
    driver.get(propertyURL)
    email_button = driver.find_element(By.XPATH, value="//button[@aria-label = 'EMAIL']")
    # get past stupid cookie button
    try:
        cookie_btn = driver.find_element(By.XPATH, value="//button[@data-tracking = 'cc-accept']")
        cookie_btn.click()
    except NoSuchElementException:
        pass
    try:
        email_button.click()
    except ElementNotInteractableException:
        email_button = driver.find_element(By.XPATH, value="//button[@data-tracking = 'email-btn']")
        email_button.click()
    
    success = True
    return success
    ### do later... dont want to actually apply yet :)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'name']").send_keys(FULLNAMEHERE)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'email']").send_keys(EMAILHERE)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'phone']").send_keys(PHONENUMBERHERE)
    # driver.find_element(By.XPATH, value="//textarea[@id = 'message']").send_keys(MESSAGEHERE)
    # driver.find_element(By.XPATH, value="//button[@aria-label = 'Send']").click()
    # time.sleep(1)

    