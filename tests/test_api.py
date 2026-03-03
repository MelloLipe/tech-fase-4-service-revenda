from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.persistence.db import veiculo_repo_instance, pagamento_repo_instance
from app.domain.entities.veiculo import Veiculo
from app.domain.entities.pagamento import Pagamento


client = TestClient(app)


def _limpar_repos():
    veiculo_repo_instance.storage.clear()
    pagamento_repo_instance.storage.clear()


class TestHealthCheck:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["service"] == "servico-principal"


class TestCadastrarVeiculoAPI:
    def setup_method(self):
        _limpar_repos()

    @patch("app.infrastructure.controllers.veiculo_controller._sincronizar_veiculo_com_servico_vendas")
    def test_cadastrar_veiculo(self, mock_sync):
        response = client.post("/veiculos/", json={
            "marca": "Toyota", "modelo": "Corolla",
            "ano": 2023, "cor": "Branco", "preco": 120000.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["marca"] == "Toyota"
        assert data["modelo"] == "Corolla"
        assert data["status"] == "DISPONIVEL"
        mock_sync.assert_called_once()


class TestEditarVeiculoAPI:
    def setup_method(self):
        _limpar_repos()

    @patch("app.infrastructure.controllers.veiculo_controller._sincronizar_veiculo_com_servico_vendas")
    def test_editar_veiculo(self, mock_sync):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_repo_instance.salvar(v)
        response = client.put(f"/veiculos/{v.id}", json={
            "cor": "Prata", "preco": 115000.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["cor"] == "Prata"
        assert data["preco"] == 115000.0

    def test_editar_veiculo_nao_encontrado(self):
        response = client.put("/veiculos/nao_existe", json={"cor": "Prata"})
        assert response.status_code == 404


class TestListarVeiculosAPI:
    def setup_method(self):
        _limpar_repos()

    def test_listar_veiculos(self):
        v1 = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v2 = Veiculo(marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=95000.0)
        veiculo_repo_instance.salvar(v1)
        veiculo_repo_instance.salvar(v2)
        response = client.get("/veiculos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_listar_vazio(self):
        response = client.get("/veiculos/")
        assert response.status_code == 200
        assert response.json() == []


class TestBuscarVeiculoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_buscar_veiculo(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_repo_instance.salvar(v)
        response = client.get(f"/veiculos/{v.id}")
        assert response.status_code == 200
        assert response.json()["marca"] == "Toyota"

    def test_buscar_veiculo_nao_encontrado(self):
        response = client.get("/veiculos/nao_existe")
        assert response.status_code == 404


class TestWebhookPagamentoAPI:
    def setup_method(self):
        _limpar_repos()

    @patch("app.infrastructure.controllers.pagamento_controller._notificar_servico_vendas_status_pagamento")
    def test_webhook_pago(self, mock_notificar):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        veiculo_repo_instance.salvar(v)
        p = Pagamento(veiculo_id=v.id, cpf_comprador="12345678901", valor=120000.0)
        pagamento_repo_instance.salvar(p)
        response = client.post("/pagamentos/webhook", json={
            "codigo_pagamento": p.codigo_pagamento, "status": "PAGO"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_status"] == "PAGO"
        mock_notificar.assert_called_once()

    @patch("app.infrastructure.controllers.pagamento_controller._notificar_servico_vendas_status_pagamento")
    def test_webhook_cancelado(self, mock_notificar):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        veiculo_repo_instance.salvar(v)
        p = Pagamento(veiculo_id=v.id, cpf_comprador="12345678901", valor=120000.0)
        pagamento_repo_instance.salvar(p)
        response = client.post("/pagamentos/webhook", json={
            "codigo_pagamento": p.codigo_pagamento, "status": "CANCELADO"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_status"] == "CANCELADO"

    def test_webhook_pagamento_nao_encontrado(self):
        response = client.post("/pagamentos/webhook", json={
            "codigo_pagamento": "nao_existe", "status": "PAGO"
        })
        assert response.status_code == 404


class TestRegistrarPagamentoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_registrar_pagamento(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_repo_instance.salvar(v)
        response = client.post(f"/pagamentos/registrar?veiculo_id={v.id}&cpf_comprador=12345678901")
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_id"] == v.id
        assert data["cpf_comprador"] == "12345678901"
        assert data["valor"] == 120000.0

    def test_registrar_pagamento_veiculo_nao_encontrado(self):
        response = client.post("/pagamentos/registrar?veiculo_id=nao_existe&cpf_comprador=12345678901")
        assert response.status_code == 400

    def test_registrar_pagamento_veiculo_indisponivel(self):
        v = Veiculo(marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v.marcar_vendido()
        veiculo_repo_instance.salvar(v)
        response = client.post(f"/pagamentos/registrar?veiculo_id={v.id}&cpf_comprador=12345678901")
        assert response.status_code == 400


class TestBuscarPagamentoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_buscar_pagamento(self):
        p = Pagamento(veiculo_id="v1", cpf_comprador="12345678901", valor=120000.0)
        pagamento_repo_instance.salvar(p)
        response = client.get(f"/pagamentos/{p.codigo_pagamento}")
        assert response.status_code == 200
        assert response.json()["veiculo_id"] == "v1"

    def test_buscar_pagamento_nao_encontrado(self):
        response = client.get("/pagamentos/nao_existe")
        assert response.status_code == 404
