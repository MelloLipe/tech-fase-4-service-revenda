import httpx
from fastapi import APIRouter, HTTPException

from app.application.dtos.pagamento_dto import WebhookPagamentoDTO
from app.application.usecases.processar_webhook_pagamento import ProcessarWebhookPagamento
from app.application.usecases.registrar_pagamento import RegistrarPagamento
from app.infrastructure.persistence.db import pagamento_repo_instance, veiculo_repo_instance
from app.config.config import settings

router = APIRouter()


@router.post("/webhook")
def webhook_pagamento(dados: WebhookPagamentoDTO):
    use_case = ProcessarWebhookPagamento(pagamento_repo_instance, veiculo_repo_instance)
    try:
        resultado = use_case.execute(dados.codigo_pagamento, dados.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    pagamento = pagamento_repo_instance.buscar_por_codigo(dados.codigo_pagamento)
    if pagamento:
        _notificar_servico_vendas_status_pagamento(
            pagamento.veiculo_id, dados.status, dados.codigo_pagamento
        )

    return resultado


@router.post("/registrar")
def registrar_pagamento(veiculo_id: str, cpf_comprador: str):
    use_case = RegistrarPagamento(pagamento_repo_instance, veiculo_repo_instance)
    try:
        pagamento = use_case.execute(veiculo_id, cpf_comprador)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return pagamento.to_dict()


@router.get("/{codigo_pagamento}")
def buscar_pagamento(codigo_pagamento: str):
    pagamento = pagamento_repo_instance.buscar_por_codigo(codigo_pagamento)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento nao encontrado")
    return pagamento.to_dict()


def _notificar_servico_vendas_status_pagamento(veiculo_id: str, status: str, codigo_pagamento: str):
    try:
        httpx.put(
            f"{settings.SALES_SERVICE_URL}/veiculos/{veiculo_id}/status-pagamento",
            json={"status": status, "codigo_pagamento": codigo_pagamento},
            timeout=5.0,
        )
    except httpx.RequestError:
        pass
