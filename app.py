from crypt import methods
from math import ceil
import os
from db import get_db
from flask import Flask, g, render_template, request, redirect, url_for

import routes.auth as auth
import routes.admin as admin
from utils.topics_helper import get_topics, get_user_score, insert_score

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


@app.route('/topic/quiz', methods=['GET', 'POST'])
@auth.login_required
def quiz_attempt():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    questions = get_db().execute(
        f"SELECT * FROM questions where topic_id = '{topic_id}'"
    ).fetchall()
    correction_map = {dict(x)['id']: dict(x)['correct'] for x in questions}
    print('correction_map', correction_map)
    if request.method == 'POST':
        max_score = len(questions)
        score = 0
        for question_id, answer in request.form.items():
            print('question_id', question_id, answer, 'right ans is:',
                  correction_map[int(question_id)])
            if int(answer) == correction_map[int(question_id)]:
                score += 1
        res_score = ceil((score/max_score)*100)
        print('quiz score', f'{score}/{max_score}= {res_score}%')
        insert_score(res_score, topic_id, int(g.user['id']))
        return redirect(url_for('quiz_result', topic_id=topic_id, score=0))
    else:
        print('topic data', topic_id, topic)
        return render_template('quiz.html',
                               topic=topic,
                               questions=enumerate(questions),
                               )


@app.route('/topic/quiz/result')
@auth.login_required
def quiz_result():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    user_score = get_user_score(topic_id, g.user['id'])
    return render_template('quiz_result.html', topic=topic, score=int(user_score['score']))


app.run(host='0.0.0.0', port=3000, debug=True)
