FROM ubuntu
RUN apt-get update && apt-get install -y apt-transport-https python3-dev python3-pip
ADD . /dbot
RUN pip3 install -r /dbot/requirements.txt
RUN source /dbot/venv/bin/activate
RUN python3 /dbot/run.py