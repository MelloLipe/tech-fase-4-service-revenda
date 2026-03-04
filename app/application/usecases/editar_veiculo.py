from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.entities.veiculo import Veiculo
from app.application.dtos.veiculo_dto import EditarVeiculoDTO


class EditarVeiculo:
    def __init__(self, repo: VeiculoRepository):
        self.repo = repo

    def execute(self, veiculo_id: str, dados: EditarVeiculoDTO) -> Veiculo:
        veiculo = self.repo.buscar_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")
        veiculo.editar(
            marca=dados.marca,
            modelo=dados.modelo,
            ano=dados.ano,
            cor=dados.cor,
            preco=dados.preco,
        )
        self.repo.atualizar(veiculo)
        return veiculo
