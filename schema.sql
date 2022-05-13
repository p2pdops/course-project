DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS quizzes;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  password TEXT
);

CREATE TABLE subjects (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  description TEXT
);

CREATE TABLE topics (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  content     TEXT,
  subject_id  INTEGER,
  FOREIGN KEY(subject_id) REFERENCES subjects(id)
);

CREATE TABLE questions (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  question  TEXT,
  option1  TEXT,
  option2  TEXT,
  option3  TEXT,
  option4  TEXT,
  correct INTEGER,
  topic_id   INTEGER,
  FOREIGN KEY(topic_id) REFERENCES topics(id)
);

CREATE TABLE user_scores (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  score     INTEGER,
  topic_id  INTEGER,
  user_id   INTEGER,
  FOREIGN KEY(topic_id) REFERENCES topics(id),
  FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users (name, email, password)
VALUES ('Admin User', 'admin@admin.com', '---'),
       ('Pavan', 'p2pdops@gmail.com', 'pbkdf2:sha256:260000$TWRqOPaOAXJWACbb$7bcbca60531103f6687814d8b99c5765e223d92837b13b05b3cf79b77d92d2b3');

INSERT INTO subjects (name, description)
VALUES ('C Programming', 'C is a general-purpose computer programming language'),
      ('Python', 'Python is a high-level, interpreted, general-purpose programming language.');

INSERT INTO topics (name, content, subject_id)
VALUES ('Variables', '## C Variables concept', 1 ),
        ('Functions', '## C Functions concept', 1 ),
        ('Pointers', '## C Pointers concept', 1 );

INSERT INTO topics (name, content, subject_id)
VALUES ('Variables', '## Python Variables concept', 2 ),
        ('Conditionals', '## Python Conditionals', 2 ),
        ('Comprehensions', '##  Python Comprehensions concept', 2 );