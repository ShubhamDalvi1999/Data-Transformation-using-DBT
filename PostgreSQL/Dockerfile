ARG POSTGIS_VERSION
FROM postgis/postgis:${POSTGIS_VERSION}

ENV POSTGRES_PASSWORD: ${DB_ADMIN_PASSWORD}

COPY Schema_definitions/ /docker-entrypoint-initdb.d/