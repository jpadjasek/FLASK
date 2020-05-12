FROM python:3.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "./main.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip

RUN mkdir workspace
WORKDIR workspace
COPY /app /workspace/app

COPY main.py /workspace/main.py
COPY requirements.txt /workspace/requirements.txt
RUN ls -la /workspace

RUN pip3 install -r requirements.txt

RUN ls -la /workspace/app

EXPOSE 5000

CMD flask run --host=0.0.0.0
