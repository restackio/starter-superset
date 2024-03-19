FROM apache/superset:3.1.1
# Switching to root to install the required packages
USER root

RUN apt-get update                             \
&& apt-get install -y --no-install-recommends \
   ca-certificates curl firefox-esr           \
# && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin 
# && apt-get purge -y ca-certificates curl

# Switching back to using the `superset` user
USER superset
