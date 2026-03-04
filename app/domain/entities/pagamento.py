import uuid
from datetime import datetime, timezone


class Pagamento:
    def __init__(self, veiculo_id: str, cpf_comprador: str, valor: float):
        self.id = str(uuid.uuid4())
        self.veiculo_id = veiculo_id
        self.cpf_comprador = cpf_comprador
        self.valor = valor
        self.codigo_pagamento = str(uuid.uuid4())
        self.status = "PENDENTE"
        self.data_venda = datetime.now(timezone.utc).isoformat()
        self.created_at = datetime.now(timezone.utc).isoformat()

    def confirmar(self):
        self.status = "PAGO"

    def cancelar(self):
        self.status = "CANCELADO"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "veiculo_id": self.veiculo_id,
            "cpf_comprador": self.cpf_comprador,
            "valor": self.valor,
            "codigo_pagamento": self.codigo_pagamento,
            "status": self.status,
            "data_venda": self.data_venda,
            "created_at": self.created_at,
        }
