FROM python:3.7.2-slim AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/
WORKDIR /app

RUN python manage.py collectstatic --no-input

FROM nginx:alpine

COPY --from=build /app/static /usr/share/nginx/html/static

RUN chmod 755 $(find /usr/share/nginx/html -type d) && chmod 644 $(find /usr/share/nginx/html -type f)

EXPOSE 80