FROM tensorflow/tensorflow:2.2.0

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" \
    apt-get -y install tzdata

RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata


COPY ./app/requirements.txt /tmp
RUN  pip install --upgrade pip && pip install -r /tmp/requirements.txt

RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords rslp

ENV FLASK_APP=api.py

EXPOSE 5000

WORKDIR /app

COPY ./app /app

CMD ["uwsgi","app.ini"]
