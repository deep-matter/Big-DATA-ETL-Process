from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash
from flask import Flask
import sqlalchemy
from flask_login import LoginManager
from flask import Blueprint, url_for, render_template, redirect, request, Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_bootstrap import Bootstrap
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo
from models import db, Users

login = Blueprint('login', __name__, static_url_path='/static',
                  static_folder='../frontend/static',
                  template_folder='../frontend/template')
login_manager = LoginManager()
login_manager.init_app(login)




@login.route('/login', methods=['GET', 'POST'])
def loginup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return render_template('home.html')
            else:
                return redirect(url_for('login.loginup') + '?error=incorrect-password')
        else:
            return redirect(url_for('login.loginup') + '?error=user-not-found')
    else:
        return render_template('login.html')


@login.route('/register', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('login.singup') + '?error=user-or-email-exists')

                return redirect(url_for('login.loginup') + '?success=account-created')
        else:
            return redirect(url_for('login.singup') + '?error=missing-fields')
    else:
        return render_template('login.html')