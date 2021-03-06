FROM ubuntu:20.04
MAINTAINER Jan Philipp Bittner

RUN apt-get update && apt-get upgrade -y \
&& apt-get install -y python3 python3-pip python3-venv hugo bibutils git make python3-virtualenv python3-wheel libyaml-dev util-linux \
&& adduser --disabled-password --gecos "" build-user \
&& mkdir -p /home/build-user/ 

ADD . /home/build-user/ir-anthology
WORKDIR /home/build-user/ir-anthology
RUN chown -R build-user:build-user /home/build-user/ \
&& runuser -u build-user -- python3 -m venv venv \
&& runuser -u build-user -- bash -c ". \"venv/bin/activate\"" \
&& runuser -u build-user -- pip3 install wheel Cython \
&& runuser -u build-user -- pip3 install -r bin/requirements.txt

ENTRYPOINT ["bash", "-c", "bin/docker_entrypoint.sh"]
