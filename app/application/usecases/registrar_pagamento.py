from app.domain.entities.pagamento import Pagamento
from app.domain.repositories.pagamento_repository import PagamentoRepository
from app.domain.repositories.veiculo_repository import VeiculoRepository


class RegistrarPagamento:
    def __init__(self, pagamento_repo: PagamentoRepository, veiculo_repo: VeiculoRepository):
        self.pagamento_repo = pagamento_repo
        self.veiculo_repo = veiculo_repo

    def execute(self, veiculo_id: str, cpf_comprador: str) -> Pagamento:
        veiculo = self.veiculo_repo.buscar_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")
        if veiculo.status != "DISPONIVEL":
            raise ValueError("Veiculo nao esta disponivel para venda")

        veiculo.marcar_vendido()
        self.veiculo_repo.atualizar(veiculo)

        pagamento = Pagamento(
            veiculo_id=veiculo_id,
            cpf_comprador=cpf_comprador,
            valor=veiculo.preco,
        )
        self.pagamento_repo.salvar(pagamento)
        return pagamento
