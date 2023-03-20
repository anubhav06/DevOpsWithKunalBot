# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-u" , "-m" , "twitterBot.py", "--host=0.0.0.0"]
EXPOSE 8080/tcp