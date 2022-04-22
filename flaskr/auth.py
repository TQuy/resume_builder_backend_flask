from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db, User
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(
                    username = username,
                    password = generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("hello"))
        flash(error)
    return render_template('auth/register.html', error=error)
