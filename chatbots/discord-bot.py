import requests
import discord.ext
from discord.ui import Button, View

apiToken = input("Please enter discord API Token: ")
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
        button = Button(label="Apply to property?", style=discord.ButtonStyle.blurple, emoji="🏠")
        async def button_callback(interaction):
            await interaction.response.send_message("hi")
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await message.channel.send("this is a test response", view=view)


def authenticateDaft():
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  }

    url = "https://auth.daft.ie/auth/realms/daft/login-actions/authenticate?session_code=1tEmQrYYRPvH8oxM5JFnnBHBVAlad7OHrtMSQIuGFCw&execution=8760aa85-3800-4a5f-8fba-7da1fc8df1ec&client_id=daft-web-v1&tab_id=OGwZPo1uZ0s"
    with requests.Session() as s:
        r = s.post(url, headers=headers, data="username=USERNAME&password=PASSWORD&rememberMe=on&webbr_fp=7a018cedd6e726fdf9d71f016bedf34c")
        print(r.text)
        print(r.status_code)

