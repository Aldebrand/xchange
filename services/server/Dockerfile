FROM python:3.8

ENV WORKDIR=/usr/src/xchange
ENV PYTHONPATH=${WORKDIR}

WORKDIR ${WORKDIR}

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install --upgrade pip && \
    pip install pipenv && \ 
    pipenv install --dev

ENTRYPOINT ["/bin/bash", "services/server/entrypoint.sh"]