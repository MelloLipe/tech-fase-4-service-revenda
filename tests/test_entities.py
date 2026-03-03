from app.domain.entities.veiculo import Veiculo
from app.domain.entities.pagamento import Pagamento


class TestVeiculo:
    def test_criar_veiculo(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        assert v.marca == "Toyota"
        assert v.modelo == "Corolla"
        assert v.ano == 2023
        assert v.cor == "Branco"
        assert v.preco == 120000.0
        assert v.status == "DISPONIVEL"
        assert v.id is not None
        assert v.created_at is not None

    def test_editar_veiculo(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.editar(marca="Honda", cor="Preto", preco=100000.0)
        assert v.marca == "Honda"
        assert v.modelo == "Corolla"
        assert v.cor == "Preto"
        assert v.preco == 100000.0

    def test_editar_veiculo_parcial(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.editar(cor="Prata")
        assert v.marca == "Toyota"
        assert v.cor == "Prata"
        assert v.preco == 120000.0

    def test_editar_veiculo_nenhum_campo(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.editar()
        assert v.marca == "Toyota"
        assert v.modelo == "Corolla"

    def test_marcar_vendido(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        assert v.status == "VENDIDO"

    def test_marcar_pago(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_pago()
        assert v.status == "PAGO"

    def test_marcar_cancelado(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_cancelado()
        assert v.status == "CANCELADO"

    def test_to_dict(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        d = v.to_dict()
        assert d["marca"] == "Toyota"
        assert d["modelo"] == "Corolla"
        assert d["ano"] == 2023
        assert d["cor"] == "Branco"
        assert d["preco"] == 120000.0
        assert d["status"] == "DISPONIVEL"
        assert "id" in d
        assert "created_at" in d


class TestPagamento:
    def test_criar_pagamento(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        assert p.veiculo_id == "v1"
        assert p.cpf_comprador == "12345678901"
        assert p.valor == 120000.0
        assert p.status == "PENDENTE"
        assert p.codigo_pagamento is not None
        assert p.id is not None

    def test_confirmar_pagamento(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        p.confirmar()
        assert p.status == "PAGO"

    def test_cancelar_pagamento(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        p.cancelar()
        assert p.status == "CANCELADO"

    def test_to_dict(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        d = p.to_dict()
        assert d["veiculo_id"] == "v1"
        assert d["cpf_comprador"] == "12345678901"
        assert d["valor"] == 120000.0
        assert d["status"] == "PENDENTE"
        assert "id" in d
        assert "codigo_pagamento" in d
        assert "data_venda" in d
        assert "created_at" in d
