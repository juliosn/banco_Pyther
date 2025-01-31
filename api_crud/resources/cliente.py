from flask_restful import Resource, reqparse
from models.cliente import ClienteModel

class Cliente(Resource):
    def get(self, id=None):
        if id:
            cliente = ClienteModel.query.get(id)
            if cliente:
                return cliente.json()
            return {'message': 'Cliente nao encontrado'}, 404
        else:
            clientes = ClienteModel.query.all()
            return [cliente.json() for cliente in clientes], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', required=True, help="Nome nao pode ser vazio")
        parser.add_argument('telefone', required=True, help="Telefone nao pode ser vazio")
        parser.add_argument('correntista', type=bool, required=True, help="Correntista deve ser booleano")
        parser.add_argument('saldo_cc', type=float, required=True, help="Saldo de conta corrente nao pode ser vazio")
        
        dados = parser.parse_args()

        if len(str(dados['telefone'])) < 11 or len(str(dados['telefone'])) > 15:
            return {'message': 'O telefone deve ter entre 11 e 15 caracteres'}, 400

        if not dados['nome'] or dados['nome'] is None:
            return {'message': 'Nome não pode ser vazio'}, 400
        if not dados['telefone'] or dados['telefone'] is None:
            return {'message': 'Telefone não pode ser vazio'}, 400
        if dados['correntista'] is None:
            return {'message': 'Correntista deve ser especificado (True/False)'}, 400
        if dados['saldo_cc'] is None:
            return {'message': 'Saldo de conta corrente não pode ser vazio'}, 400

        cliente = ClienteModel(**dados)
        cliente.save_to_db()

        return cliente.json(), 201

    def put(self, id):
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

        if not dados['nome'] or dados['nome'] is None:
            return {'message': 'Nome nao pode ser vazio'}, 400
        if not dados['telefone'] or dados['telefone'] is None:
            return {'message': 'Telefone nao pode ser vazio'}, 400
        if dados['correntista'] is None:
            return {'message': 'Correntista deve ser especificado (True/False)'}, 400
        if dados['saldo_cc'] is None:
            return {'message': 'Saldo de conta corrente nao pode ser vazio'}, 400

        cliente.nome = dados['nome']
        cliente.telefone = dados['telefone']
        cliente.correntista = dados['correntista']
        cliente.saldo_cc = dados['saldo_cc']
        cliente.save_to_db()

        return cliente.json(), 200

    def delete(self, id):
        cliente = ClienteModel.query.get(id)
        if not cliente:
            return {'message': 'Cliente nao encontrado'}, 404

        cliente.delete_from_db()
        return {'message': 'Cliente excluído'}, 200
