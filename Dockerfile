FROM python:3.11.9-slim-bookworm

COPY zjuintl_assistant /app/zjuintl_assistant
COPY api.py /app/api.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3", "api.py"]
