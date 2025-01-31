from flask import Flask
from flask_restful import Api
from resources.cliente import Cliente
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_request
def cria_banco():
    banco.create_all()

api.add_resource(Cliente, '/api/v1/clientes', '/api/v1/clientes/<int:id>')

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True, port=5001)
