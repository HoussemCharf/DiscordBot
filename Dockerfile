FROM ubuntu
RUN apt-get update && apt-get install -y apt-transport-https python3-dev python3-pip
ADD . /dbot
RUN pip3 install -r requirements.txt
CMD ["export","bot_token=TOKEN"]
CMD ['python3','/dbot/run.py']
