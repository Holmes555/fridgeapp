#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $USERNAME;
	CREATE DATABASE $DBNAME;
	GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $USERNAME;
EOSQL
