from sql_alchemy import banco

class ClienteModel(banco.Model):
    __tablename__ = 'clientes'
    
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    telefone = banco.Column(banco.String(20))
    correntista = banco.Column(banco.Boolean)
    saldo_cc = banco.Column(banco.Float)

    def __init__(self, nome, telefone, correntista, saldo_cc):
        self.nome = nome
        self.telefone = telefone
        self.correntista = correntista
        self.saldo_cc = saldo_cc

    def save_to_db(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_from_db(self):
        banco.session.delete(self)
        banco.session.commit()

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'correntista': self.correntista,
            'saldo_cc': self.saldo_cc
        }
