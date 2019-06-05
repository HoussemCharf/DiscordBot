FROM ubuntu
RUN apt-get update && apt-get install -y apt-transport-https python3-dev python3-pip screen
ADD . /dbot
RUN pip3 install -r /dbot/requirements.txt
CMD ["source","/dbot/venv/bin/activate"]
CMD ['screen','python3','/dbot/run.py']
