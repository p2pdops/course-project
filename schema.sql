-- Create table  IF NOT EXISTSs users, subjects, topics, quizzes

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS quizzes;


CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  password TEXT
);
INSERT INTO users (name, email, password) VALUES ('Admin User', 'admin@admin.com', '---');

CREATE TABLE  IF NOT EXISTS subjects (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  description TEXT
);

CREATE TABLE  IF NOT EXISTS topics (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  content     TEXT,
  subject_id  INTEGER,
  FOREIGN KEY(subject_id) REFERENCES subjects(id)
);

CREATE TABLE  IF NOT EXISTS quizzes (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT,
  topic_id  INTEGER,
  FOREIGN KEY(topic_id) REFERENCES topics(id)
);

-- Create table  IF NOT EXISTSs questions, answers, and choices

CREATE TABLE  IF NOT EXISTS questions (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  question  TEXT,
  quiz_id   INTEGER,
  FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
);

CREATE TABLE  IF NOT EXISTS answers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  answer      TEXT,
  question_id INTEGER,
  FOREIGN KEY(question_id) REFERENCES questions(id)
);

CREATE TABLE  IF NOT EXISTS choices (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  choice      TEXT,
  correct     INTEGER,
  question_id INTEGER,
  FOREIGN KEY(question_id) REFERENCES questions(id)
);

-- Create table  IF NOT EXISTSs scores, and users_scores

CREATE TABLE  IF NOT EXISTS scores (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  score     INTEGER,
  quiz_id   INTEGER,
  user_id   INTEGER,
  FOREIGN KEY(quiz_id) REFERENCES quizzes(id),
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- CREATE TABLE  IF NOT EXISTS users_scores (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
