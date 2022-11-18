FROM python:3.7-slim-buster

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y curl ffmpeg libsm6 libxext6

WORKDIR ./app
COPY requirements.txt requirements.txt 
COPY ./main.py ./
COPY ./src ./src

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD [ "python3", "-m", "main"]
