FROM faishol27/gunicorn:latest

COPY src/requirements.txt .
RUN apk --no-cache add py3-pip python3-dev && \
    pip3 install -r requirements.txt && rm requirements.txt && \
    apk del py3-pip python3-dev

ENV GUNICORN_WSGI_MODULE=website.wsgi:application
COPY src .
RUN chmod +x *.sh

entrypoint ["./start.sh"]