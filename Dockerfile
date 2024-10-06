# Use an official Python image as a base
FROM python:3.12-slim

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# Install system dependencies needed for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    gcc

# Set the working directory in the container
WORKDIR /app

ADD . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Change working directory in the container
WORKDIR /app/mysite

# Run the Django app
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:$PORT mysite.wsgi:application"]

# Release latest changes to docker and heroku (On windows)
# docker build -t project2-backend . ; heroku container:push web --app group16-project2 ; heroku container:release web --app group16-project2
