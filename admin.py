import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.before_app_request
def load_admin_loggedin():
    admin_logged_in = session.get('admin_logged_in')
    if admin_logged_in is None:
        g.admin = None
    else:
        g.admin = True


@bp.route('/subjects')
def subjects_list():
    subjects = get_db().execute(
        'SELECT * FROM subjects'
    ).fetchall()
    return render_template(
        'admin/subjects-list.html',
        subtitle="Admin/ Subjects/ all",
        subjects=subjects
    )


@bp.route('/subjects/show')
def subjects_show():
    subject_id = request.args.get('subject_id')
    subject = get_db().execute(
        f"SELECT * FROM subjects where id = '{subject_id}'"
    ).fetchone()
    topics = get_db().execute(
        f"SELECT * FROM topics where subject_id = '{subject_id}'"
    ).fetchall()
    print('subject data', subject_id, subject)
    return render_template(
        'admin/subjects-show.html',
        subtitle="Admin/ Subjects/ Show",
        subject=subject,
        topics=topics,
    )


@bp.route('/create-subject', methods=('GET', 'POST'))
def create_subject():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()
        error = None
        if not name:
            error = 'Subject name is required.'
        if error is None:
            try:
                db.execute(f"INSERT INTO subjects (name) VALUES ('{name}')")
                db.commit()
            except db.IntegrityError:
                error = f"Subject {name} is already registered."
            else:
                return redirect(url_for("admin.subjects_list"))
        flash(error)
    else:
        return render_template('admin/create-subject.html')


@bp.route('/create-topic', methods=('GET', 'POST'))
def create_topic():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        name = request.form['name']
        db = get_db()
        error = None
        if not name:
            error = 'Subject name is required.'
        if error is None:
            try:
                db.execute(f"INSERT INTO subjects (name) VALUES ('{name}')")
                db.commit()
            except db.IntegrityError:
                error = f"Topic {name} is already registered."
            else:
                return redirect(url_for("admin.subjects_show", subject_id=subject_id))
        flash(error)
    else:
        return render_template('admin/create-topic.html')


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
