# Dockerfile, image, Container
FROM python:3.8

ADD test.py .
COPY requirements.txt requirements.txt

RUN pip3 pip3 install -r requirements.txt

CMD ["python", "./test.py"]