from flask import Flask, request, jsonify
from config import config  # Corrigido o nome do módulo para 'config' em minúsculo, compatível com o padrão do Python.
from Models import db, bcrypt, User  # Certifique-se de que 'Models.py' está correto.

app = Flask(__name__)  # Cria uma instância do Flask, que é o aplicativo web.
app.config.from_object(config)  # Carrega as configurações a partir da classe 'config'.

db.init_app(app)  # Inicializa o banco de dados com a instância do Flask.
bcrypt.init_app(app)  # Inicializa o Bcrypt com a instância do Flask.

# Certifique-se de criar todas as tabelas no banco de dados ao inicializar a aplicação
with app.app_context():
    db.create_all()

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()  # Obtém os dados enviados no corpo da requisição no formato JSON.
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():  # Corrigido o nome para 'User' (classe definida em Models).
        return jsonify({'error': 'Email já cadastrado'}), 400

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = User.query.all()  # Corrigido para usar 'User' (classe definida em Models).
    usuarios_list = [
        {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email}
        for usuario in usuarios
    ]
    return jsonify(usuarios_list), 200

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask em modo de depuração.
