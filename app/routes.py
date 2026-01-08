from flask import Blueprint, render_template



rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def home():
    return render_template('home.html')