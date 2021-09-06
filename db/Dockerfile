FROM postgres:alpine
RUN apk update
RUN apk add grep
RUN whoami
ADD init-db/init-db.sql /docker-entrypoint-initdb.d/
COPY shell_scripts /db/shell_scripts
RUN chmod -R 555 /docker-entrypoint-initdb.d && chmod -R 555 /db/shell_scripts
EXPOSE 5432