import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.before_app_request
def load_admin_loggedin():
    admin_logged_in = session.get('admin')
    if admin_logged_in is None:
        g.admin = None
        login_path = url_for('auth.login')
        if request.path != login_path:
            return redirect(login_path)
    else:
        g.admin = True
        g.user = get_db().execute("SELECT * FROM users WHERE id = '1'").fetchone()


@bp.route('/')
def admin_home():
    subjects = get_db().execute(
        'SELECT * FROM subjects'
    ).fetchall()
    return render_template(
        'admin/index.html',
        subtitle="Admin/ Subjects/ all",
        subjects=subjects
    )


@bp.route('/subjects/create', methods=('GET', 'POST'))
def create_subject():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        error = None
        if not name:
            error = 'Subject name is required.'
        if error is None:
            try:
                db.execute(
                    f"INSERT INTO subjects(name, description) " +
                    f"VALUES('{name}', '{description}')")
                db.commit()
            except db.IntegrityError:
                error = f"Subject {name} is already registered."
            else:
                return redirect(url_for("admin.admin_home"))
        flash(error)
    else:
        return render_template('admin/subject-create.html')


@bp.route('/subjects/show')
def subjects_show():
    subject_id = request.args.get('subject_id')
    subject = get_db().execute(
        f"SELECT * FROM subjects where id = '{subject_id}'"
    ).fetchone()
    topics = get_db().execute(
        f"SELECT * FROM topics where subject_id = '{subject_id}'"
    ).fetchall()
    print('subject data', subject_id, subject, topics)
    return render_template(
        'admin/subjects-show.html',
        subtitle="Admin/ Subjects/ Show",
        subject=subject,
        topics=topics,
    )


@bp.route('/topic/create', methods=('GET', 'POST'))
def create_topic():
    subject_id = request.args.get('subject_id')
    if request.method == 'POST':
        name = request.form['name']
        # description = request.form['description']
        content = request.form['content']
        db = get_db()
        error = None
        if not name:
            error = 'Subject name is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO topics (name, content, subject_id) " +
                    " VALUES (?, ?, ?)",
                    (name, content, subject_id)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Topic {name} is already registered."
            else:
                return redirect(url_for("admin.subjects_show", subject_id=subject_id))
        flash(error)
    else:
        return render_template('admin/topic-create.html', subject_id=subject_id)


@bp.route('/topic/show')
def topic_show():
    topic_id = request.args.get('topic_id')
    topic = get_db().execute(
        f"SELECT * FROM topics where id = '{topic_id}'"
    ).fetchone()
    print('topic data', topic_id, topic)
    return render_template('admin/topic-show.html', topic=topic)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
