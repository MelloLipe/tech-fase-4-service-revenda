import uuid
from datetime import datetime, timezone


class Veiculo:
    def __init__(self, marca: str, modelo: str, ano: int, cor: str, preco: float):
        self.id = str(uuid.uuid4())
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.preco = preco
        self.status = "DISPONIVEL"
        self.created_at = datetime.now(timezone.utc).isoformat()

    def editar(self, marca: str = None, modelo: str = None, ano: int = None,
               cor: str = None, preco: float = None):
        if marca is not None:
            self.marca = marca
        if modelo is not None:
            self.modelo = modelo
        if ano is not None:
            self.ano = ano
        if cor is not None:
            self.cor = cor
        if preco is not None:
            self.preco = preco

    def marcar_vendido(self):
        self.status = "VENDIDO"

    def marcar_pago(self):
        self.status = "PAGO"

    def marcar_cancelado(self):
        self.status = "CANCELADO"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "cor": self.cor,
            "preco": self.preco,
            "status": self.status,
            "created_at": self.created_at,
        }
