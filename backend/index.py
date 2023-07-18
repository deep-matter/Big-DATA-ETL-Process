from flask import Blueprint, redirect, render_template

index = Blueprint('index', __name__,  static_url_path='/static',
                  static_folder='../frontend/static',
                  template_folder='../frontend/template')


@index.route('/', methods=['GET'])
def show():
    return render_template('login.html')
