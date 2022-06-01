FROM ubuntu:latest
MAINTAINER Iulian Serbanoiu <undergraver@gmail.com>
COPY analyze.py /root
RUN apt update -y
RUN apt install -y python3-minimal
CMD ["/root/analyze.py", "-h"]

