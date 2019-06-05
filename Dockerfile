FROM ubuntu
RUN apt-get update && apt-get install -y apt-transport-https python3-dev
ADD . /
RUN pip install -r requirements.txt
CMD ["export","bot_token=TOKEN"]
CMD ['python3','./run.py']
