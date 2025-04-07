import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from config import config
from Models import db, bcrypt, User

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'supersecretkey'

CORS(app)

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado'}), 400

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = User.query.filter_by(email=email).first()
    if usuario and usuario.check_senha(senha):
        session['user_id'] = usuario.id
        session['user_name'] = usuario.nome
        return jsonify({'message': 'Login bem-sucedido'}), 200
    return jsonify({'error': 'Credenciais inválidas'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return jsonify({'message': 'Logout bem-sucedido'}), 200

@app.route('/usuario', methods=['GET'])
def get_usuario():
    user_id = session.get('user_id')
    if user_id:
        usuario = User.query.get(user_id)
        return jsonify({'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email}), 200
    return jsonify({'error': 'Usuário não logado'}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
