import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        print('g.user', g.user)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    else:
        return render_template('auth/register.html')


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

        if email == 'admin@admin.com' and password == 'admin':
            session.clear()
            session['admin'] = True
            return redirect(url_for('admin.admin_home'))

        if user is None:
            error = 'Incorrect email. ' + email
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password. ' + email

        if error is None:
            print("Login success")
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home_page'))
        print('Error while login: ', error)
    else:
        return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None and request.path != '/auth/login' and request.path != '/auth/register':
            print("Login required")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
