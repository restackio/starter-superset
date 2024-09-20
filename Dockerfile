# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP superset

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    default-libmysqlclient-dev

# Install Python dependencies
RUN pip install --upgrade pip setuptools
RUN pip install apache-superset

# Copy the custom superset_config.py file
COPY superset_config.py /app/superset_config.py

# Set the PYTHONPATH to include /app
ENV PYTHONPATH=/app:$PYTHONPATH

# Set the SUPERSET_CONFIG environment variable
ENV SUPERSET_CONFIG superset_config

# Initialize the database
RUN superset db upgrade

# Create an admin user (change username and password as needed)
RUN superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin

# Load examples and create default roles/permissions
RUN superset load_examples
RUN superset init

# Make port 8088 available to the world outside this container
EXPOSE 80

# Run Superset
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "--timeout", "120", "--limit-request-line", "0", "--limit-request-field_size", "0", "superset.app:create_app()"]
