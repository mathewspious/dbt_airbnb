FROM --platform=linux/amd64 python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends

WORKDIR /root/.dbt

WORKDIR /usr/src/dbt

# Install the dbt Postgres adapter. This step will also install dbt-core
RUN pip install --upgrade pip
RUN pip install dbt-postgres==1.9.0
RUN pip install pytz

# Install dbt dependencies (as specified in packages.yml file)
# Build seeds, models and snapshots (and run tests wherever applicable)
CMD dbt deps && dbt build ; sleep infinity