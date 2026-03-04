from app.infrastructure.persistence.db import InMemoryVeiculoRepository, InMemoryPagamentoRepository
from app.domain.entities.veiculo import Veiculo
from app.domain.entities.pagamento import Pagamento


class TestInMemoryVeiculoRepository:
    def setup_method(self):
        self.repo = InMemoryVeiculoRepository()

    def test_salvar_e_buscar(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(v)
        resultado = self.repo.buscar_por_id(v.id)
        assert resultado is not None
        assert resultado.marca == "Toyota"

    def test_buscar_inexistente(self):
        resultado = self.repo.buscar_por_id("nao_existe")
        assert resultado is None

    def test_listar_todos(self):
        v1 = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v2 = Veiculo(marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=95000.0)
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        todos = self.repo.listar_todos()
        assert len(todos) == 2

    def test_listar_vazio(self):
        todos = self.repo.listar_todos()
        assert len(todos) == 0

    def test_atualizar(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(v)
        v.editar(cor="Prata")
        self.repo.atualizar(v)
        resultado = self.repo.buscar_por_id(v.id)
        assert resultado.cor == "Prata"


class TestInMemoryPagamentoRepository:
    def setup_method(self):
        self.repo = InMemoryPagamentoRepository()

    def test_salvar_e_buscar_por_codigo(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        self.repo.salvar(p)
        resultado = self.repo.buscar_por_codigo(p.codigo_pagamento)
        assert resultado is not None
        assert resultado.veiculo_id == "v1"

    def test_buscar_por_codigo_inexistente(self):
        resultado = self.repo.buscar_por_codigo("nao_existe")
        assert resultado is None

    def test_buscar_por_veiculo_id(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        self.repo.salvar(p)
        resultado = self.repo.buscar_por_veiculo_id("v1")
        assert resultado is not None
        assert resultado.cpf_comprador == "12345678901"

    def test_buscar_por_veiculo_id_inexistente(self):
        resultado = self.repo.buscar_por_veiculo_id("nao_existe")
        assert resultado is None

    def test_atualizar(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        self.repo.salvar(p)
        p.confirmar()
        self.repo.atualizar(p)
        resultado = self.repo.buscar_por_codigo(p.codigo_pagamento)
        assert resultado.status == "PAGO"
