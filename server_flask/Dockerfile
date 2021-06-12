FROM pytorch
MAINTAINER Beomsoo

ENV PATH=/opt/conda/bin:$PATH

RUN apt-get -y install python-pip
RUN pip install flask kss wget whoosh sentence_transformers fairseq pymongo xmltodict pytube3 pytube transformers marisa-trie
RUN python -m pip install --upgrade pytube
RUN pip3 install git+https://github.com/ssuwani/pytube 

RUN mkdir -p server
WORKDIR /server
COPY . /server
#ENV PATH=/opt/conda/bin:$PATH

ENTRYPOINT ["/bin/bash", "./settings.sh"]
