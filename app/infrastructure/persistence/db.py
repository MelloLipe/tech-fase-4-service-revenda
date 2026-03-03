from typing import Optional
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.entities.veiculo import Veiculo
from app.domain.repositories.pagamento_repository import PagamentoRepository
from app.domain.entities.pagamento import Pagamento


class InMemoryVeiculoRepository(VeiculoRepository):
    def __init__(self):
        self.storage: dict[str, Veiculo] = {}

    def salvar(self, veiculo: Veiculo) -> None:
        self.storage[veiculo.id] = veiculo

    def buscar_por_id(self, veiculo_id: str) -> Optional[Veiculo]:
        return self.storage.get(veiculo_id)

    def listar_todos(self) -> list[Veiculo]:
        return list(self.storage.values())

    def atualizar(self, veiculo: Veiculo) -> None:
        self.storage[veiculo.id] = veiculo


class InMemoryPagamentoRepository(PagamentoRepository):
    def __init__(self):
        self.storage: dict[str, Pagamento] = {}

    def salvar(self, pagamento: Pagamento) -> None:
        self.storage[pagamento.id] = pagamento

    def buscar_por_codigo(self, codigo_pagamento: str) -> Optional[Pagamento]:
        for pagamento in self.storage.values():
            if pagamento.codigo_pagamento == codigo_pagamento:
                return pagamento
        return None

    def buscar_por_veiculo_id(self, veiculo_id: str) -> Optional[Pagamento]:
        for pagamento in self.storage.values():
            if pagamento.veiculo_id == veiculo_id:
                return pagamento
        return None

    def atualizar(self, pagamento: Pagamento) -> None:
        self.storage[pagamento.id] = pagamento


veiculo_repo_instance = InMemoryVeiculoRepository()
pagamento_repo_instance = InMemoryPagamentoRepository()
