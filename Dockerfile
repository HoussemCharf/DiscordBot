FROM houssemcharf/discordlucina
RUN apt-get update && apt-get install -y apt-transport-https python3-dev git ffmpeg libopus-dev libffi-dev libsodium-dev python3-pip 
WORKDIR /dbot
RUN pip3 install -r /dbot/requirements.txt