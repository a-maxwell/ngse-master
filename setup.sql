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
  form_type_id INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(form_type_id)
);

CREATE TABLE version(
  ver_id INTEGER NOT NULL,
  form_type_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL,
  created_by INTEGER NOT NULL,
  PRIMARY KEY (ver_id)
);

CREATE TABLE lifetime_of_forms(
  date_started TIMESTAMP NOT NULL,
  date_ended TIMESTAMP NOT NULL,
  ver_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL,
  created_by INTEGER NOT NULL, /* ID of admin/dept head (?) */
  PRIMARY KEY (date_started, date_ended, ver_id)
);

CREATE TABLE categories(
  category_id INTEGER NOT NULL,
  category TEXT NOT NULL,
  date_created TIMESTAMP NOT NULL,
  created_by INTEGER NOT NULL,
  PRIMARY KEY (category_id)
);

CREATE TABLE questions(
  question_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  form_type_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL,
  ver_id INTEGER, /* temporary null */
  category_id INTEGER NOT NULL,
  /*input_type TEXT*/
  PRIMARY KEY (question_id)
);

CREATE TABLE user_types(
  user_type_id INTEGER NOT NULL,
  type VARCHAR(50) NOT NULL,
  PRIMARY KEY (user_type_id)
);

CREATE TABLE users(
  user_id INTEGER NOT NULL,
  email VARCHAR(50),
  password_salt VARCHAR(250),
  password_hash VARCHAR(250) NOT NULL,
  user_type_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, user_type_id)
);

CREATE TABLE answers(
  answer_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  answer TEXT,
  PRIMARY KEY (answer_id)
);

CREATE TABLE recommenders(
  recommender_id INTEGER NOT NULL,
  rank INTEGER NOT NULL,
  email VARCHAR(50) NOT NULL,
  password_salt VARCHAR(250) NOT NULL,
  password_hash VARCHAR(250) NOT NULL,
  user_id INTEGER NOT NULL, /* ID of the applicant he/she recommends */
  PRIMARY KEY (recommender_id, user_id)
);

INSERT INTO users (user_id, email, password_hash, user_type_id) VALUES (1, 'admin@admin.com', 'password', 1);
