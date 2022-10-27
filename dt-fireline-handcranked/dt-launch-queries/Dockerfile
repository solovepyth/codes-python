FROM python:3.8-slim-buster

LABEL maintainer="data.digital@telma.mg"

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip setuptools wheel

RUN groupadd -g 2000 telma && useradd -u 2000 -g telma -s /bin/sh telma
# USER telma:telma

ENV WORKDIR=/app
ENV APPLICATION_NAME=dt-telmashops-mfs-1.0.dev0

#COPY --chown=telma:telma ./target/dist ${WORKDIR}/
COPY ./target/dist ${WORKDIR}/

RUN pip install -e ${WORKDIR}/${APPLICATION_NAME}

ENTRYPOINT ["run"]

