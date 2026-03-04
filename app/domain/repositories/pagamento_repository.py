from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.pagamento import Pagamento


class PagamentoRepository(ABC):
    @abstractmethod
    def salvar(self, pagamento: Pagamento) -> None:
        pass

    @abstractmethod
    def buscar_por_codigo(self, codigo_pagamento: str) -> Optional[Pagamento]:
        pass

    @abstractmethod
    def buscar_por_veiculo_id(self, veiculo_id: str) -> Optional[Pagamento]:
        pass

    @abstractmethod
    def atualizar(self, pagamento: Pagamento) -> None:
        pass
