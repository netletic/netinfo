FROM python:3.9

LABEL maintainer="Jarno Timmermans"

RUN groupadd -r netinfo && useradd -r -g netinfo netinfo
RUN chsh -s /usr/sbin/nologin root
WORKDIR /home/netinfo

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY rfc1925.txt .
COPY main.py .

CMD ["python", "main.py"]
