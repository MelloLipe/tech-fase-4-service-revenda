from pydantic import BaseModel
from typing import Optional


class CriarVeiculoDTO(BaseModel):
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: float


class EditarVeiculoDTO(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
    cor: Optional[str] = None
    preco: Optional[float] = None


class VeiculoResponseDTO(BaseModel):
    id: str
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: float
    status: str
    created_at: str
