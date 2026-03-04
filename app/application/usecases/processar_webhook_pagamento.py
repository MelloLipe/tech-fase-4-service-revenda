from app.domain.repositories.pagamento_repository import PagamentoRepository
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.domain.entities.pagamento import Pagamento


class ProcessarWebhookPagamento:
    def __init__(self, pagamento_repo: PagamentoRepository, veiculo_repo: VeiculoRepository):
        self.pagamento_repo = pagamento_repo
        self.veiculo_repo = veiculo_repo

    def execute(self, codigo_pagamento: str, status: str) -> dict:
        pagamento = self.pagamento_repo.buscar_por_codigo(codigo_pagamento)
        if not pagamento:
            raise ValueError("Pagamento nao encontrado")

        veiculo = self.veiculo_repo.buscar_por_id(pagamento.veiculo_id)
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")

        if status == "PAGO":
            pagamento.confirmar()
            veiculo.marcar_pago()
        elif status == "CANCELADO":
            pagamento.cancelar()
            veiculo.marcar_cancelado()
        else:
            raise ValueError("Status invalido. Use PAGO ou CANCELADO")

        self.pagamento_repo.atualizar(pagamento)
        self.veiculo_repo.atualizar(veiculo)

        return {
            "pagamento": pagamento.to_dict(),
            "veiculo_status": veiculo.status,
        }
