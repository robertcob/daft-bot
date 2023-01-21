FROM python:3
ADD requirements.txt /
ADD main.py /
RUN pip install -r requirements.txt
ADD chatsbots/ scraper/ 
CMD [ "python", "./main.py" ]