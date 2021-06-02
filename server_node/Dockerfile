#1. install nodeJS
FROM node:14.16.0
MAINTAINER Beomsoo

#2-1. Python
RUN apt-get update
RUN apt install -y git
RUN apt-get install -y python3-pip
RUN apt-get install -y python-pip
RUN pip install youtube-transcript-api

#2-3. Install node_modules
RUN mkdir -p /server
WORKDIR /server
COPY . .
RUN npm install
RUN npm install yarn

#3. move file to virtual environment
RUN chmod 755 ./start_server.sh

#4. CMD
ENTRYPOINT [ "/bin/bash", "./start_server.sh" ]



