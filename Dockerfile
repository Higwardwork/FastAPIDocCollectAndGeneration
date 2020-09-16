FROM python:3.8.5-windowsservercore-1809
COPY ./app /app

WORKDIR /app/
ENV PYTHONUNBUFFERED 1
ENV COMPOSE_CONVERT_WINDOWS_PATHS=1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/app

EXPOSE 8080

CMD [".app/main.py"]