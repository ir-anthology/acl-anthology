FROM ubuntu:20.04
MAINTAINER Jan Philipp Bittner

RUN apt-get update && apt-get upgrade -y \
&& apt-get install -y python3 python3-pip python3-venv hugo bibutils git make python3-virtualenv python3-wheel libyaml-dev util-linux \
&& adduser --disabled-password --gecos "" build-user \
&& mkdir -p /home/build-user/ \
&& chown -R build-user:build-user /home/build-user/ \
&& runuser -u build-user -- pip3 install black docopt filetype iso-639 latexcodec lxml nltk pre-commit pybtex python-slugify PyYAML requests stop-words texsoup tqdm wheel

WORKDIR /home/build-user
#RUN git clone https://github.com/acl-org/acl-anthology

ADD acl-anthology /home/build-user/acl-anthology
#RUN chown -R build-user:build-user /home/build-user/acl-anthology
#USER build-user:build-user
WORKDIR /home/build-user/acl-anthology
#this has to be done manually, because its not done in the make file and one cant directly invoke the venv target
#because it overwrites the venv/bin/activate 
#i dont understand why they did it that way in the make file
RUN python3 -m venv venv
RUN bash -c ". \"venv/bin/activate\" && pip3 install wheel Cython && pip3 install -r bin/requirements.txt"

ENTRYPOINT ["bash", "-c", "/home/build-user/acl-anthology/bin/build.sh"]
