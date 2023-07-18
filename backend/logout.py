from flask import Blueprint, url_for, redirect
from flask_login import LoginManager, login_required, logout_user

logout = Blueprint('logout', __name__, static_url_path='/static',
                  static_folder='../frontend/static',
                  template_folder='../frontend/template')
login_manager = LoginManager()
login_manager.init_app(logout)

@logout.route('/logout')
@login_required
def show():
    logout_user()
    return redirect(url_for('login.loginup') + '?success=logged-out')