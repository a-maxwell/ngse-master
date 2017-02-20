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

\c ngsewebsite;

CREATE TABLE form_types(
  form_type_id SERIAL PRIMARY KEY,
  form_type TEXT NOT NULL
);

CREATE TABLE forms(
  form_id SERIAL PRIMARY KEY,
  date_start TIMESTAMP NOT NULL,
  date_end TIMESTAMP NOT NULL,
  form_type_id INTEGER NOT NULL,
  page_sequence INTEGER[] NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE categories(
  category_id SERIAL PRIMARY KEY,
  category TEXT NOT NULL,
  form_type_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE questions(
  question_id SERIAL PRIMARY KEY,
  question TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  -- form_type_id INTEGER NOT NULL,
  metadata JSONB,
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
  user_type TEXT NOT NULL
);

CREATE TABLE users(
  user_id SERIAL PRIMARY KEY,
  given_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  /*password_salt VARCHAR(250),*/
  password_hash TEXT NOT NULL,
  user_type_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE applicant_attrs(
  attr_id SERIAL PRIMARY KEY,
  erdt_status BOOLEAN NOT NULL DEFAULT FALSE,
  applicant_status INTEGER NOT NULL DEFAULT 0,
  validation_status TEXT NOT NULL DEFAULT 'incomplete',
  recommender_A INTEGER,
  recommender_B INTEGER,
  recommender_C INTEGER,
  applicant_id INTEGER UNIQUE NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT NOW(),
  last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
  constraint u_constraint UNIQUE (recommender_A, recommender_B, recommender_C)
);

INSERT INTO user_types (user_type) VALUES ('Staff'), ('Representative'), ('Applicant'), ('Recommender');
INSERT INTO form_types (form_type) VALUES ('Application Form'), ('Recommendation Letter'), ('Registration Form');

INSERT INTO users (given_name, email, password_hash, date_created, last_modified, user_type_id) VALUES ('Admin', 'ngse@engg.upd.edu.ph', 'password', '02/19/17 01:00', '02/19/17 01:00', 1);
