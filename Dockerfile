FROM apache/superset:2.1.3
# Switching to root to install the required packages
USER root

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl


# Example: installing a driver to connect to Redshift
# Find which driver you need based on the analytics database
# you want to connect to here:
# https://superset.apache.org/installation.html#database-dependencies

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache -r /app/requirements.txt
ENV REQUIREMENTS_LOCAL=/app/requirements.txt

# Example: add custom configuration
# https://superset.apache.org/docs/installation/configuring-superset/#configuring-superset
# COPY superset_config.py /app/pythonpath/superset_config.py
# ENV SUPERSET_CONFIG_PATH /app/pythonpath/superset_config.py

# Switching back to using the `superset` user
USER superset
