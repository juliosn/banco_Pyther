import unittest
from app import app, banco
from flask import json

class TestClientAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.testing = True
        cls.app = app.test_client()
        banco.init_app(app)

        with app.app_context():
            banco.create_all()

    def setUp(self):
        with app.app_context():
            for table in reversed(banco.metadata.sorted_tables):
                banco.session.execute(table.delete())
            banco.session.commit()

    def test_get_all_clients(self):
        response = self.app.get('/api/v1/conta/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_create_client(self):
        data = {
            'nome': 'Novo Cliente',
            'telefone': '123456789012',
            'correntista': True,
            'saldo_cc': 200.0
        }
        response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(response.status_code, 201)

        json_data = response.get_json()
        self.assertIn('id', json_data)
        self.assertEqual(json_data['nome'], data['nome'])

    def test_get_client_by_id(self):
        data = {'nome': 'Cliente Teste', 'telefone': '123456789012', 'correntista': True, 'saldo_cc': 500.0}
        create_response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(create_response.status_code, 201)

        client_id = create_response.get_json()['id']
        response = self.app.get(f'/api/v1/conta/clientes/{client_id}')
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['id'], client_id)
        self.assertEqual(json_data['nome'], data['nome'])

    def test_update_client(self):
        data = {'nome': 'Cliente Antigo', 'telefone': '123456789012', 'correntista': True, 'saldo_cc': 500.0}
        create_response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(create_response.status_code, 201)

        client_id = create_response.get_json()['id']
        updated_data = {'nome': 'Cliente Atualizado', 'telefone': '987654321098', 'correntista': False, 'saldo_cc': 1000.0}
        response = self.app.put(f'/api/v1/conta/clientes/{client_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['nome'], updated_data['nome'])
        self.assertEqual(json_data['telefone'], updated_data['telefone'])
        self.assertEqual(json_data['saldo_cc'], updated_data['saldo_cc'])

    def test_delete_client(self):
        data = {'nome': 'Cliente Deletável', 'telefone': '123456789012', 'correntista': True, 'saldo_cc': 500.0}
        create_response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(create_response.status_code, 201)

        client_id = create_response.get_json()['id']
        response = self.app.delete(f'/api/v1/conta/clientes/{client_id}')
        self.assertEqual(response.status_code, 200)

        get_response = self.app.get(f'/api/v1/conta/clientes/{client_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_calculate_credit_score(self):
        data = {'nome': 'Cliente Score', 'telefone': '123456789012', 'correntista': True, 'saldo_cc': 500.0}
        create_response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(create_response.status_code, 201)

        client_id = create_response.get_json()['id']
        response = self.app.get(f'/api/v1/conta/clientes/score_credito/{client_id}')
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        expected_score = data['saldo_cc'] * 0.1
        self.assertEqual(json_data['score_credito'], expected_score)

    def test_create_client_missing_name(self):
        data = {
            'telefone': '123456789012',
            'correntista': True,
            'saldo_cc': 200.0
        }
        response = self.app.post('/api/v1/conta/clientes', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Nome nao pode ser vazio", response.data.decode())

    def test_get_non_existent_client(self):
        response = self.app.get('/api/v1/conta/clientes/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Cliente nao encontrado", response.data.decode())

    def test_update_non_existent_client(self):
        updated_data = {
            'nome': 'Cliente Atualizado',
            'telefone': '987654321098',
            'correntista': False,
            'saldo_cc': 1000.0
        }
        response = self.app.put('/api/v1/conta/clientes/999', json=updated_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Cliente nao encontrado", response.data.decode())

    def test_delete_non_existent_client(self):
        response = self.app.delete('/api/v1/conta/clientes/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Cliente nao encontrado", response.data.decode())        

if __name__ == '__main__':
    unittest.main()
