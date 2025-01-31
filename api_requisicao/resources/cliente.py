from flask_restful import Resource, reqparse
import requests
from sql_alchemy import banco
from models.cliente import ClienteModel

class Cliente(Resource):
    def get(self, id=None):
        try:
            if id:
                cliente = ClienteModel.query.get(id)
                if cliente:
                    return cliente.json()
                return {'message': 'Cliente nao encontrado'}, 404
            else:
                clientes = ClienteModel.query.all()
                return [cliente.json() for cliente in clientes], 200
        except Exception as e:
            return {'message': f'Ocorreu um erro ao buscar os clientes: {str(e)}'}, 500

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nome', required=True, help="Nome nao pode ser vazio")
            parser.add_argument('telefone', required=True, help="Telefone nao pode ser vazio")
            parser.add_argument('correntista', type=bool, required=True, help="Correntista deve ser booleano")
            parser.add_argument('saldo_cc', type=float, required=True, help="Saldo de conta corrente nao pode ser vazio")

            dados = parser.parse_args()

            if len(str(dados['telefone'])) < 11 or len(str(dados['telefone'])) > 15:
                return {'message': 'O telefone deve ter entre 11 e 15 caracteres'}, 400
            if dados['correntista'] is None:
                return {'message': 'Correntista deve ser especificado (True/False)'}, 400

            cliente = ClienteModel(**dados)
            cliente.save_to_db()

            return cliente.json(), 201
        except Exception as e:
            return {'message': f'Ocorreu um erro ao criar o cliente: {str(e)}'}, 500

    def put(self, id):
        try:
            cliente = ClienteModel.query.get(id)
            if not cliente:
                return {'message': 'Cliente nao encontrado'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('nome', required=True, help="Nome nao pode ser vazio")
            parser.add_argument('telefone', required=True, help="Telefone nao pode ser vazio")
            parser.add_argument('correntista', type=bool, required=True, help="Correntista deve ser booleano")
            parser.add_argument('saldo_cc', type=float, required=True, help="Saldo de conta corrente nao pode ser vazio")

            dados = parser.parse_args()

            if len(str(dados['telefone'])) < 11 or len(str(dados['telefone'])) > 15:
                return {'message': 'O telefone deve ter entre 11 e 15 caracteres'}, 400
            if dados['correntista'] is None:
                return {'message': 'Correntista deve ser especificado (True/False)'}, 400

            cliente.nome = dados['nome']
            cliente.telefone = dados['telefone']
            cliente.correntista = dados['correntista']
            cliente.saldo_cc = dados['saldo_cc']
            cliente.save_to_db()

            return cliente.json(), 200
        except Exception as e:
            return {'message': f'Ocorreu um erro ao atualizar o cliente: {str(e)}'}, 500

    def delete(self, id):
        try:
            cliente = ClienteModel.query.get(id)
            if not cliente:
                return {'message': 'Cliente nao encontrado'}, 404

            cliente.delete_from_db()
            return {'message': 'Cliente excluído'}, 200
        except Exception as e:
            return {'message': f'Ocorreu um erro ao excluir o cliente: {str(e)}'}, 500
