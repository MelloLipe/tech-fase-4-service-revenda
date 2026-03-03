from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.veiculo import Veiculo


class VeiculoRepository(ABC):
    @abstractmethod
    def salvar(self, veiculo: Veiculo) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, veiculo_id: str) -> Optional[Veiculo]:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Veiculo]:
        pass

    @abstractmethod
    def atualizar(self, veiculo: Veiculo) -> None:
        pass
