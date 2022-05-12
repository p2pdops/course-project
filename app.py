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

app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)


@app.route('/')
@auth.login_required
def hello():
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


@app.route('/read-topic')
def read_topic():
    return render_template(
        'read-topic.html',
        subtitle="Admin/ Subjects/ Show",
    )


app.run(host='0.0.0.0', port=3000, debug=True)
