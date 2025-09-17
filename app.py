# Arquivo: backend/app.py (Versão Profissional Final)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lanchonete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- MODELOS DO BANCO DE DADOS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.String(50), nullable=False)
    itens = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Recebido')

# =======================================================================
# CÓDIGO QUE CRIA O BANCO DE DADOS E AS TABELAS AUTOMATICAMENTE
# =======================================================================
with app.app_context():
    db.create_all()

# =======================================================================
# CARDÁPIO COM ENDEREÇOS COMPLETOS DAS IMAGENS NO SEU SITE NETLIFY
# =======================================================================
menu = {
    "Lanches": [
        { "id": 1, "nome": 'Hambúrguer', "preco": 14.00, "desc": 'Pão, carne, alface, tomate, milho, queijo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/hamburguer.jpg' },
        { "id": 2, "nome": 'X-Burguer', "preco": 16.00, "desc": 'Pão, carne, alface, tomate, milho, queijo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xburguer.jpg' },
        { "id": 3, "nome": 'Egg Burguer', "preco": 17.00, "desc": 'Pão, carne, alface, tomate, milho, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/eggburguer.jpg' },
        { "id": 4, "nome": 'X-Egg', "preco": 18.00, "desc": 'Pão, carne, alface, tomate, milho, queijo, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xegg.png' },
        { "id": 5, "nome": 'X-Bacon', "preco": 18.00, "desc": 'Pão, carne, alface, tomate, milho, queijo, bacon, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xbacon.png' },
        { "id": 6, "nome": 'Egg Bacon', "preco": 19.00, "desc": 'Pão, carne, alface, tomate, milho, bacon, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xeggbacon.png' },
        { "id": 7, "nome": 'X-Egg Bacon', "preco": 20.00, "desc": 'Pão, carne, alface, tomate, milho, queijo, bacon, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xeggbacon.png' },
        { "id": 8, "nome": 'Americano', "preco": 24.00, "desc": 'Pão, carne, alface, milho, bacon, 1 queijo, 2 ovos, presunto, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/americano.png' },
        { "id": 9, "nome": 'X-Americano', "preco": 25.00, "desc": 'Pão, carne, alface, milho, queijo, presunto, bacon, banana, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xamericano.png' },
        { "id": 10, "nome": 'X-Tudo', "preco": 28.00, "desc": 'Pão, carne, alface, milho, queijo, presunto, bacon, ovo, cheddar, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xtudo.png' },
        { "id": 11, "nome": 'X-Tudo Duplo', "preco": 40.00, "desc": 'Pão, 2 carnes, alface, milho, bacon, 2 queijos, 2 presuntos, 2 ovos, cheddar em creme, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xtudoduplo.png' },
        { "id": 12, "nome": 'X-Salada', "preco": 18.00, "desc": 'Pão, filé de frango, alface, tomate, milho, queijo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xsalada.png' },
        { "id": 14, "nome": 'Frangão', "preco": 26.00, "desc": 'Pão, filé de frango, alface, tomate, milho, queijo, bacon, ovo, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/frangao.png' },
        { "id": 15, "nome": 'Frango Duplo', "preco": 30.00, "desc": 'Pão, 2 filés de frango, alface, milho, 2 queijos, bacon, presunto, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/frangaoduplo.png' },
        { "id": 16, "nome": 'X-Master Burguer', "preco": 50.00, "desc": 'Pão, 2 carnes, 2 filés de frango, 2 queijos, 2 presuntos, 2 ovos, bacon em dobro, cheddar, batata palha', "imagem": 'https://masterburguer.netlify.app/image/lanches/xmaster.png' }
    ],
    "Franguinhos & Porções": [
        { "id": 17, "nome": 'Mini 250g', "preco": 35.00, "desc": 'Acompanha 1 porção', "imagem": 'https://masterburguer.netlify.app/image/porcoes/frango250.png' },
        { "id": 18, "nome": 'Porção 500g', "preco": 65.00, "desc": 'Acompanha 2 porções', "imagem": 'https://masterburguer.netlify.app/image/porcoes/frango500.png' },
        { "id": 19, "nome": 'Porção 1Kg', "preco": 85.00, "desc": 'Acompanha 3 porções', "imagem": 'https://masterburguer.netlify.app/image/porcoes/frango1.png' },
        { "id": 20, "nome": 'Polenta', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/polenta.png' },
        { "id": 21, "nome": 'Coxinha', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/coxinha.png' },
        { "id": 22, "nome": 'Batata', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/batata.png' },
        { "id": 23, "nome": 'Batata Cheddar e Bacon', "preco": 30.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/batatab.png' },
        { "id": 24, "nome": 'Bolinho de Aipim com Queijo', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/bolinhaq.png' },
        { "id": 25, "nome": 'Bolinho de Aipim com Carne', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/bolinhac.png' },
        { "id": 26, "nome": 'Bolinho de Queijo', "preco": 18.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/porcoes/queijo.png' }
    ],
    "Bebidas": [
        { "id": 33, "nome": 'Água', "preco": 4.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/bebidas/agua.jpg' },
        { "id": 34, "nome": 'Água com Gás', "preco": 5.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/bebidas/aguagas.png' },
        { "id": 38, "nome": 'Refrigerante Lata', "preco": 6.00, "desc": 'Diversas opções', "imagem": 'https://masterburguer.netlify.app/image/bebidas/refri.jpg' },
        { "id": 40, "nome": 'Refrigerante Litro', "preco": 15.00, "desc": 'Diversas opções', "imagem": 'https://masterburguer.netlify.app/image/bebidas/refril.jpg' }
    ],
    "Cervejas": [
        { "id": 41, "nome": 'Heineken Latão', "preco": 12.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/bebidas/cerveja1.jpg' },
        { "id": 42, "nome": 'Amstel Latão', "preco": 8.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/bebidas/amstel.png' },
        { "id": 43, "nome": 'Petra Latão', "preco": 8.00, "desc": '', "imagem": 'https://masterburguer.netlify.app/image/bebidas/petra.jpeg' }
    ]
}

# --- ROTAS DA API ---
@app.route('/api/cardapio')
def get_cardapio():
    return jsonify(menu)

@app.route('/api/pedidos', methods=['POST', 'GET'])
def gerenciar_pedidos():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'mesa' not in data or 'itens' not in data:
            return jsonify({'message': 'Dados do pedido incompletos'}), 400
        novo_pedido = Pedido(
            mesa=data['mesa'],
            itens=json.dumps(data['itens']),
            status='Recebido'
        )
        db.session.add(novo_pedido)
        db.session.commit()
        return jsonify({ 'message': 'Pedido recebido com sucesso!', 'pedido_id': novo_pedido.id }), 201
    
    if request.method == 'GET':
        pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
        lista_de_pedidos = []
        for pedido in pedidos:
            lista_de_pedidos.append({
                'id': pedido.id,
                'mesa': pedido.mesa,
                'itens': json.loads(pedido.itens),
                'status': pedido.status
            })
        return jsonify(lista_de_pedidos)

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data or 'senha' not in data:
        return jsonify({'message': 'Dados incompletos!'}), 400

    user_exists = User.query.filter_by(email=data['email']).first()
    if user_exists:
        return jsonify({'message': 'Este e-mail já está cadastrado!'}), 400

    novo_usuario = User(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha']
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
