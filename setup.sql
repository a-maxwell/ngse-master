-- run:
-- sudo -u postgres psql
-- \i '<path to this file>'
--
-- example:
-- \i '/home/user/Desktop/NGSE/setup.sql'
-- then edit the file 'load_data.sql' found in the same folder
-- after that run
-- \i '<path to load_data.sql>'

\c postgres

DROP DATABASE IF EXISTS ngsewebsite;
CREATE DATABASE ngsewebsite;
CREATE USER ngse WITH PASSWORD 'ngse';
GRANT ALL PRIVILEGES ON DATABASE ngsewebsite TO ngse;