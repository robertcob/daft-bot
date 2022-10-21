import os
import discord.ext
from discord.ui import Button, View
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

global success

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    view = View()
    applyButton = Button(label="Apply to property?", style=discord.ButtonStyle.blurple, emoji="🏠")
    successButton = Button(label="Email Sent!", style=discord.ButtonStyle.green, emoji="🥳", disabled=True)
    failureButton = Button(label="Apply to property manually through URL", style=discord.ButtonStyle.red, emoji="🥳", disabled=True)
    pendingButton = Button(label="Sending Email...", style=discord.ButtonStyle.grey, emoji="🧩", disabled=True)
    view.add_item(applyButton)
    if message.content.startswith('NEW PROPERTY!'):
        content = str(message.content)
        rawLink = content.split("\n")[3]
        url = rawLink.split(' ')[4]
        async def button_callback(interaction):
            view.remove_item(applyButton)
            view.add_item(pendingButton)
            if interaction.user.id == 594871112253571103:
                await interaction.response.defer()
                newMessage = await interaction.followup.edit_message(int(interaction.message.id), content= "", view=view)
                success = applyToProperty(url)
                if success:
                    view.remove_item(pendingButton)
                    view.add_item(successButton)
                    await interaction.followup.send("🎉🎉🥳🥳 email sent successfully!")
                    await interaction.followup.edit_message(int(newMessage.id), content= "", view=view)
                else:
                    view.remove_item(pendingButton)
                    view.add_item(failureButton)
                    await interaction.followup.send("🚫🚫🚫🚫 Failed to apply for property, apply directly")
                    await interaction.followup.edit_message(int(newMessage.id), content= "", view=view)
            else:
                await interaction.followup.send("🚫🚫🚫🚫 Only bob can respond to messages")
        applyButton.callback = button_callback
        await message.channel.send("Click to apply", view=view)

def applyToProperty(propertyURL):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        authURL = "https://www.daft.ie/auth/authenticate"
        driver.get(authURL)
        driver.find_element(By.XPATH, value='''//*[@id="username"]''').send_keys(os.environ['DAFTEMAIL'])
        password = driver.find_element(By.XPATH, value='''//*[@id="password"]''')
        password.send_keys(os.environ['DAFTPASSWORD'])
        password.send_keys(Keys.ENTER)
        try:
            cookie_btn = driver.find_element(By.XPATH, value="//button[@data-tracking = 'cc-accept']")
            cookie_btn.click()
        except NoSuchElementException:
            pass
        driver.get(propertyURL)
        email_button = driver.find_element(By.XPATH, value="//button[@aria-label = 'EMAIL']")

        try:
            email_button.click()
        except ElementNotInteractableException:
            email_button = driver.find_element(By.XPATH, value="//button[@data-tracking = 'email-btn']")
            email_button.click()
        return True
    except:
        return False

    ### do later... dont want to actually apply yet :)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'name']").send_keys(FULLNAMEHERE)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'email']").send_keys(EMAILHERE)
    # driver.find_element(By.XPATH, value="//input[@aria-label = 'phone']").send_keys(PHONENUMBERHERE)
    # driver.find_element(By.XPATH, value="//textarea[@id = 'message']").send_keys(MESSAGEHERE)
    # driver.find_element(By.XPATH, value="//button[@aria-label = 'Send']").click()
    # time.sleep(1)

def run(apiToken):
    client.run(apiToken)
    