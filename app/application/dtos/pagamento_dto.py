from pydantic import BaseModel


class WebhookPagamentoDTO(BaseModel):
    codigo_pagamento: str
    status: str
