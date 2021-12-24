CREATE ROLE teacheetah WITH LOGIN PASSWORD 'TeacheetahPsWd123';
CREATE DATABASE teacheetah_db;
GRANT ALL PRIVILEGES ON DATABASE teacheetah_db TO teacheetah;
