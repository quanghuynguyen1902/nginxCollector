FROM python:3

ENV PYTHONUNBUFFERED=1
COPY . /app
RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/processor_error.py"]

