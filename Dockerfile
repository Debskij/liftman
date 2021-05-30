FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1

COPY liftman /liftman

ENTRYPOINT ["python", "-m", "liftman"]