FROM python:3.8

# ADD src/parse-results.py

RUN pip install requirements.txt

CMD ["python", "./main.py"]