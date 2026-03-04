from app.domain.entities.veiculo import Veiculo
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.application.dtos.veiculo_dto import CriarVeiculoDTO


class CadastrarVeiculo:
    def __init__(self, repo: VeiculoRepository):
        self.repo = repo

    def execute(self, dados: CriarVeiculoDTO) -> Veiculo:
        veiculo = Veiculo(
            marca=dados.marca,
            modelo=dados.modelo,
            ano=dados.ano,
            cor=dados.cor,
            preco=dados.preco,
        )
        self.repo.salvar(veiculo)
        return veiculo
