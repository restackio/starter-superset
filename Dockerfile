FROM apache/superset:2.1.0 AS lean

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8 \
  FLASK_ENV=production \
  FLASK_APP="superset.app:create_app()" \
  PYTHONPATH="/app/pythonpath" \
  SUPERSET_HOME="/app/superset_home" \
  SUPERSET_PORT=8088

USER root

# Upstream base and updates
RUN mkdir -p ${SUPERSET_HOME} ${PYTHONPATH} \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends \
  build-essential \
  default-libmysqlclient-dev \
  libsasl2-modules-gssapi-mit \
  libpq-dev \
  nano \
  && rm -rf /var/lib/apt/lists/*

# Authlib for Oauth2; impyla, mysql, and ascend for database connectors
RUN pip install --no-cache \
  Authlib \
  mysqlclient \
  'impyla>=0.17.0'

# snowflake-sqlalchemy 1.3.1 requires sqlalchemy>1.4.0, but that currently breaks superset, so we'll pin to 1.2.4 of snowflake for now
RUN pip install --no-cache \
  'snowflake-sqlalchemy==1.2.4'

# prophet for forecasting
RUN pip install --no-cache \
  'pystan<3.0.0' \
  tqdm \
  lunarcalendar \
  && pip install --no-cache \
  prophet

WORKDIR /app

USER superset

HEALTHCHECK CMD curl -f "http://localhost:$SUPERSET_PORT/health"

EXPOSE ${SUPERSET_PORT}

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]