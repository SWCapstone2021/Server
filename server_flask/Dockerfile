FROM server_flask
MAINTAINER Beomsoo

ENV PATH=/opt/conda/bin:$PATH

RUN apt-get -y install openssl
RUN pip3 install flask
RUN pip install youtube_transcript_api
RUN apt-get -y install python-pip

RUN apt-get -y install software-properties-common 
# RUN add-apt-repository ppa:certbot/certbot :: Enter
RUN apt-get update
RUN apt-get install certbot 

RUN mkdir -p server
WORKDIR /server
COPY . /server
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650 -passout pass:abcd -subj "/C=KR/ST=Seoul/L=Seoul/O=42Seoul/OU=Lee/CN=localhost"

#ENV PATH=/opt/conda/bin:$PATH

ENTRYPOINT [ "/bin/bash", "./settings.sh" ]
