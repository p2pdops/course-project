import os
from db import get_db
from flask import Flask, g, render_template, request

import routes.auth as auth
import routes.admin as admin
from utils.topics_helper import get_topics

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join('data', 'database.sqlite'),
)

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)


@app.route('/')
@auth.login_required
def home_page():
    subjects = get_db().execute(
        'SELECT * FROM subjects'
    ).fetchall()
    return render_template('index.html', subjects=subjects)


@app.route('/subjects/show')
@auth.login_required
def subjects_show():
    subject_id = request.args.get('subject_id')
    subject = get_db().execute(
        f"SELECT * FROM subjects where id = '{subject_id}'"
    ).fetchone()
    topics = get_topics(subject_id, g.user['id'])
    print('subject data', subject_id, subject)
    return render_template('subject.html', subject=subject,
                           topics=topics,
                           )


@app.route('/topic/read')
@auth.login_required
def read_topic():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    print('topic data', topic_id, topic)
    return render_template('topic.html', topic=topic)


@app.route('/topic/quiz')
@auth.login_required
def quiz_attempt():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    questions = get_db().execute(
        f"SELECT * FROM questions where topic_id = '{topic_id}'"
    ).fetchall()

    print('topic data', topic_id, topic)
    return render_template('quiz.html',
                           topic=topic,
                           questions=enumerate(questions),
                           )


app.run(host='0.0.0.0', port=3000, debug=True)
