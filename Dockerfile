FROM python:3
ADD requirements.txt /
ADD main.py /
ADD chatbots/config.ini / chatbots/discordBot.py / chatbots/discordMessageSend.py /
ADD scraper/daftLibrary.py /
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]