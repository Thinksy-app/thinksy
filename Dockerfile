FROM python:3.11.4-slim-buster as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.11.4-slim-buster as app
WORKDIR /app/
COPY *.py /app/
RUN mkdir /app/app/
COPY app/*.py /app/app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
ENTRYPOINT python main.py