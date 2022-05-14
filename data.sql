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

INSERT INTO questions (question, option1, option2, option3, option4, correct, topic_id)
VALUES ('What is the output of the following code? \n\n int a = 10; \n int b = 20; \n int c = a + b; \n printf("%d", c);', '30', '20', '30', '40', 1),
        ('What is size of int32?', '1 Byte', '2 Byte', '3 Byte', '4 Byte', 2,1),
        ('How to access value in pointer in C?', '&ptr', '*ptr', 'ptr','::ptr',2);