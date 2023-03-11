FROM python:3.10-alpine3.17

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

WORKDIR /usr/app

ENTRYPOINT ["python3"]
CMD ["src/app.py"]
