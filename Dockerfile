FROM ubuntu:20.04

RUN apt update &&     apt upgrade -y &&     apt install -y python python3-pip curl
COPY requirements.txt /config/requirements.txt 
RUN pip install -r /config/requirements.txt 
RUN pip install pyuwsgi
RUN pip install mysql-connector-python -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./src /app

WORKDIR /app

#CMD [ "flask", "--app", "server", "--debug", "run", "-h", "0.0.0.0"]
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--master", "-p", "4", "-w", "server:app"]
