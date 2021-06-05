FROM python:3.9

LABEL maintainer="Jarno Timmermans"

RUN groupadd -r netinfo && useradd -r -g netinfo netinfo
RUN chsh -s /usr/sbin/nologin root
WORKDIR /home/netinfo

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
