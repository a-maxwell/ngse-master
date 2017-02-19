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

\c ngsewebsite;

/*
DROP TABLE form_types;
DROP TABLE versions;
DROP TABLE lifetime_of_forms;
DROP TABLE categories;
DROP TABLE questions;
DROP TABLE user_types;
DROP TABLE users;
DROP TABLE recommenders;
DROP TABLE answers;
*/

CREATE TABLE form_types(
  form_type_id SERIAL PRIMARY KEY,
  form_type VARCHAR(50) NOT NULL
);

CREATE TABLE cycles(
  cycle_id SERIAL PRIMARY KEY,
  date_start TIMESTAMP NOT NULL,
  date_end TIMESTAMP NOT NULL,
  form_type_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
);

CREATE TABLE categories(
  category_id SERIAL PRIMARY KEY,
  category TEXT UNIQUE NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE questions(
  question_id SERIAL PRIMARY KEY,
  question TEXT UNIQUE NOT NULL,
  category_id INTEGER NOT NULL,
  form_type_id INTEGER NOT NULL,
  -- cycle_id INTEGER, /* temporary null */
  /*input_type TEXT*/
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE answers(
  answer_id SERIAL PRIMARY KEY,
  answer TEXT,
  question_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE user_types(
  user_type_id SERIAL PRIMARY KEY,
  user_type VARCHAR(50) NOT NULL
);

CREATE TABLE users(
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(50) UNIQUE,
  /*password_salt VARCHAR(250),*/
  password_hash VARCHAR(250) NOT NULL,
  user_type_id INTEGER NOT NULL,
  owner_id INTEGER,
  rank INTEGER,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO user_types (user_type) VALUES ('Staff'), ('Representative'), ('Applicant'), ('Recommender');
INSERT INTO form_types (form_type) VALUES ('Application Form'), ('Recommendation Letter');

INSERT INTO users (email, password_hash, date_created, last_modified, user_type_id) VALUES ('ngse@engg.upd.edu.ph', 'password', '02/19/17 01:00', '02/19/17 01:00', 1);
