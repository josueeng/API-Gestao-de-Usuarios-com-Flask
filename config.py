import os

# Calcula o diretório base do arquivo atual
basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TESTE'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dados.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
