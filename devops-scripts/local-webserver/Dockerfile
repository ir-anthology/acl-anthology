FROM ubuntu:20.04
MAINTAINER Jan Philipp Bittner

RUN apt-get update && apt-get upgrade -y && apt-get install -y nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]
