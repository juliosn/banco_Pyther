from flask import Flask, request
from flask_restful import Api
from models.cliente import ClienteModel
from resources.cliente import Cliente
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Cliente, '/api/v1/conta/clientes', '/api/v1/conta/clientes/<int:id>')

@app.route('/api/v1/conta/clientes/score_credito/<int:id>', methods=['GET'])
def calcular_score_credito(id):
    cliente = ClienteModel.query.get(id)
    if not cliente:
        return {'message': 'Cliente não encontrado'}, 404
    score = cliente.saldo_cc * 0.1
    return {'score_credito': score}, 200

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True, port=5000)

    with app.app_context():
        banco.create_all() 