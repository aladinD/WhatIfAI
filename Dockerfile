FROM ubuntu
LABEL maintainer "n.landerer@tum.de"

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt install python3 -y

RUN apt-get update && apt-get install python3-pip -y

RUN pip3 install --upgrade setuptools

RUN pip3 install numpy==1.18.4
RUN pip3 install pandas==1.0.3
RUN pip3 install convertdate==2.2.1
RUN pip3 install LunarCalendar==0.0.9
RUN pip3 install holidays==0.10.2
RUN pip3 install matplotlib==3.2.1
RUN pip3 install plotly==4.8.1
RUN pip3 install pystan==2.19.1.1

COPY dependencies/requirements.txt /usr/bin
RUN pip3 install -U -r /usr/bin/requirements.txt

#ENTRYPOINT tail -f /dev/null
ENTRYPOINT python3 /mnt/host/main.py
