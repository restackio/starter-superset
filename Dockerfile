FROM apache/superset:2.1.0
# Switching to root to install the required packages
USER root

# Example: installing a driver to connect to Redshift
# Find which driver you need based on the analytics database
# you want to connect to here:
# https://superset.apache.org/installation.html#database-dependencies

RUN pip install snowflake-sqlalchemy==1.2.4
RUN pip install sqlalchemy-redshift==0.8.14

# Example: add custom configuration
# https://superset.apache.org/docs/installation/configuring-superset/#configuring-superset
COPY superset_config.py /app/superset_config.py
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

# Switching back to using the `superset` user
USER superset