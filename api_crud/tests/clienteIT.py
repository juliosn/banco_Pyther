import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from sql_alchemy import banco
from models.cliente import ClienteModel

class TestClientAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.testing = True
        
        banco.init_app(app)
        cls.app = app.test_client()

        with app.app_context():
            banco.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            banco.session.remove()
            banco.drop_all()

    def tearDown(self):
        with app.app_context():
            banco.session.rollback()
            for table in reversed(banco.metadata.sorted_tables):
                banco.session.execute(table.delete())
            banco.session.commit()

    def test_get_all_clients(self):
        response = self.app.get('/api/v1/clientes')
        self.assertEqual(response.status_code, 200)

    def test_create_client(self):
        data = {
            'nome': 'Novo Cliente',
            'telefone': '123456789012',
            'correntista': True,
            'saldo_cc': 200.0
        }
        response = self.app.post('/api/v1/clientes', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Novo Cliente', response.data.decode())

    def test_delete_client(self):
        with app.app_context():
            cliente = ClienteModel(nome='Cliente Deletado', telefone='12345678900', correntista=True, saldo_cc=0.0)
            banco.session.add(cliente)
            banco.session.commit()
            banco.session.refresh(cliente)

        response = self.app.delete(f'/api/v1/clientes/{cliente.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_client(self):
        with app.app_context():
            cliente = ClienteModel(nome='Teste', telefone='12345678900', correntista=True, saldo_cc=100.0)
            banco.session.add(cliente)
            banco.session.commit()
            banco.session.refresh(cliente)

        response = self.app.get(f'/api/v1/clientes/{cliente.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Teste', response.data.decode())

    def test_update_client(self):
        with app.app_context():
            cliente = ClienteModel(nome='Cliente Atual', telefone='12345678900', correntista=False, saldo_cc=150.0)
            banco.session.add(cliente)
            banco.session.commit()
            banco.session.refresh(cliente)

            data = {
                'nome': 'Cliente Atualizado',
                'telefone': '98765432100',
                'correntista': True,
                'saldo_cc': 300.0
            }

        response = self.app.put(f'/api/v1/clientes/{cliente.id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cliente Atualizado', response.data.decode())

    def test_create_client_invalid_data(self):
        data = {
            'nome': 'Novo Cliente',
            'telefone': '12345',
            'correntista': True,
            'saldo_cc': 200.0
        }
        response = self.app.post('/api/v1/clientes', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("O telefone deve ter entre 11 e 15 caracteres", response.data.decode())

    def test_get_non_existent_client(self):
        response = self.app.get('/api/v1/clientes/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Cliente nao encontrado", response.data.decode())

    def test_delete_non_existent_client(self):
        response = self.app.delete('/api/v1/clientes/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Cliente nao encontrado', response.data.decode())

    def test_update_non_existent_client(self):
        response = self.app.put('/api/v1/clientes/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Cliente nao encontrado', response.data.decode())

    def test_update_client_invalid_data(self):
        with app.app_context():
            cliente = ClienteModel(nome='Cliente Atual', telefone='12345678900', correntista=False, saldo_cc=150.0)
            banco.session.add(cliente)
            banco.session.commit()
            banco.session.refresh(cliente)

        data = {
            'nome': 'Cliente Atualizado',
            'telefone': '12345',
            'correntista': True,
            'saldo_cc': 300.0
        }

        response = self.app.put(f'/api/v1/clientes/{cliente.id}', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("O telefone deve ter entre 11 e 15 caracteres", response.data.decode())

    def test_create_client_missing_required_field(self):
        data = {
            'telefone': '123456789012',
            'correntista': True,
            'saldo_cc': 200.0
        }
        response = self.app.post('/api/v1/clientes', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nome nao pode ser vazio', response.data.decode())

if __name__ == '__main__':
    unittest.main()
