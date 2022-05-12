import os
from db import get_db
from flask import Flask, render_template, request

import auth
import admin

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
def subjects_show():
    subject_id = request.args.get('subject_id')
    subject = get_db().execute(
        f"SELECT * FROM subjects where id = '{subject_id}'"
    ).fetchone()
    topics = get_db().execute(
        f"SELECT * FROM topics where subject_id = '{subject_id}'"
    ).fetchall()
    print('subject data', subject_id, subject)
    return render_template('subject.html', subject=subject,
                           topics=topics,
                           )


@app.route('/topic/read')
def read_topic():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    print('topic data', topic_id, topic)
    return render_template('topic.html', topic=topic)


app.run(host='0.0.0.0', port=3000, debug=True)
