FROM ubuntu
RUN apt-get install python3-dev
ADD . /
RUN pip3 install requirement.txt -y
CMD ["export","bot_token=TOKEN"]
CMD ['python3','./run.py']
