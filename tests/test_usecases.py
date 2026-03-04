import pytest
from app.infrastructure.persistence.db import InMemoryVeiculoRepository, InMemoryPagamentoRepository
from app.domain.entities.veiculo import Veiculo
from app.domain.entities.pagamento import Pagamento
from app.application.dtos.veiculo_dto import CriarVeiculoDTO, EditarVeiculoDTO
from app.application.usecases.cadastrar_veiculo import CadastrarVeiculo
from app.application.usecases.editar_veiculo import EditarVeiculo
from app.application.usecases.registrar_pagamento import RegistrarPagamento
from app.application.usecases.processar_webhook_pagamento import ProcessarWebhookPagamento


class TestCadastrarVeiculo:
    def setup_method(self):
        self.repo = InMemoryVeiculoRepository()
        self.use_case = CadastrarVeiculo(self.repo)

    def test_cadastrar(self):
        dto = CriarVeiculoDTO(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo = self.use_case.execute(dto)
        assert veiculo.marca == "Toyota"
        assert veiculo.status == "DISPONIVEL"
        assert self.repo.buscar_por_id(veiculo.id) is not None


class TestEditarVeiculo:
    def setup_method(self):
        self.repo = InMemoryVeiculoRepository()
        self.use_case = EditarVeiculo(self.repo)

    def test_editar(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(v)
        dto = EditarVeiculoDTO(cor="Prata", preco=115000.0)
        resultado = self.use_case.execute(v.id, dto)
        assert resultado.cor == "Prata"
        assert resultado.preco == 115000.0

    def test_editar_nao_encontrado(self):
        dto = EditarVeiculoDTO(cor="Prata")
        with pytest.raises(ValueError, match="Veiculo nao encontrado"):
            self.use_case.execute("nao_existe", dto)


class TestRegistrarPagamento:
    def setup_method(self):
        self.veiculo_repo = InMemoryVeiculoRepository()
        self.pagamento_repo = InMemoryPagamentoRepository()
        self.use_case = RegistrarPagamento(self.pagamento_repo, self.veiculo_repo)

    def test_registrar(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.veiculo_repo.salvar(v)
        pagamento = self.use_case.execute(v.id, "12345678901")
        assert pagamento.veiculo_id == v.id
        assert pagamento.cpf_comprador == "12345678901"
        assert pagamento.valor == 120000.0
        assert pagamento.status == "PENDENTE"
        veiculo_atualizado = self.veiculo_repo.buscar_por_id(v.id)
        assert veiculo_atualizado.status == "VENDIDO"

    def test_registrar_veiculo_nao_encontrado(self):
        with pytest.raises(ValueError, match="Veiculo nao encontrado"):
            self.use_case.execute("nao_existe", "12345678901")

    def test_registrar_veiculo_indisponivel(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        self.veiculo_repo.salvar(v)
        with pytest.raises(ValueError, match="Veiculo nao esta disponivel"):
            self.use_case.execute(v.id, "12345678901")


class TestProcessarWebhookPagamento:
    def setup_method(self):
        self.veiculo_repo = InMemoryVeiculoRepository()
        self.pagamento_repo = InMemoryPagamentoRepository()
        self.use_case = ProcessarWebhookPagamento(self.pagamento_repo, self.veiculo_repo)

    def _criar_veiculo_e_pagamento(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        self.veiculo_repo.salvar(v)
        p = Pagamento(veiculo_id=v.id, cpf_comprador="12345678901", valor=120000.0)
        self.pagamento_repo.salvar(p)
        return v, p

    def test_processar_pago(self):
        v, p = self._criar_veiculo_e_pagamento()
        resultado = self.use_case.execute(p.codigo_pagamento, "PAGO")
        assert resultado["veiculo_status"] == "PAGO"
        assert resultado["pagamento"]["status"] == "PAGO"

    def test_processar_cancelado(self):
        v, p = self._criar_veiculo_e_pagamento()
        resultado = self.use_case.execute(p.codigo_pagamento, "CANCELADO")
        assert resultado["veiculo_status"] == "CANCELADO"
        assert resultado["pagamento"]["status"] == "CANCELADO"

    def test_processar_status_invalido(self):
        v, p = self._criar_veiculo_e_pagamento()
        with pytest.raises(ValueError, match="Status invalido"):
            self.use_case.execute(p.codigo_pagamento, "INVALIDO")

    def test_processar_pagamento_nao_encontrado(self):
        with pytest.raises(ValueError, match="Pagamento nao encontrado"):
            self.use_case.execute("nao_existe", "PAGO")

    def test_processar_veiculo_nao_encontrado(self):
        p = Pagamento(veiculo_id="nao_existe", cpf_comprador="12345678901", valor=120000.0)
        self.pagamento_repo.salvar(p)
        with pytest.raises(ValueError, match="Veiculo nao encontrado"):
            self.use_case.execute(p.codigo_pagamento, "PAGO")
