FROM python:3-alpine3.21

ARG GID=1000
ARG UID=1000

RUN echo $GID
RUN mkdir /app \
    && addgroup -g $GID user \
    && adduser --disabled-password --ingroup user --uid $UID user

USER user

COPY --chown=user:user app/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

COPY app /app

WORKDIR /app

CMD ["/app/main.py"]
