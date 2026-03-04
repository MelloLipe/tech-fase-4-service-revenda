import httpx
from fastapi import APIRouter, HTTPException

from app.application.dtos.veiculo_dto import CriarVeiculoDTO, EditarVeiculoDTO
from app.application.usecases.cadastrar_veiculo import CadastrarVeiculo
from app.application.usecases.editar_veiculo import EditarVeiculo
from app.infrastructure.persistence.db import veiculo_repo_instance
from app.config.config import settings

router = APIRouter()


@router.post("/")
def cadastrar_veiculo(dados: CriarVeiculoDTO):
    use_case = CadastrarVeiculo(veiculo_repo_instance)
    veiculo = use_case.execute(dados)
    _sincronizar_veiculo_com_servico_vendas(veiculo.to_dict())
    return veiculo.to_dict()


@router.put("/{veiculo_id}")
def editar_veiculo(veiculo_id: str, dados: EditarVeiculoDTO):
    use_case = EditarVeiculo(veiculo_repo_instance)
    try:
        veiculo = use_case.execute(veiculo_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    _sincronizar_veiculo_com_servico_vendas(veiculo.to_dict())
    return veiculo.to_dict()


@router.get("/")
def listar_veiculos():
    veiculos = veiculo_repo_instance.listar_todos()
    return [v.to_dict() for v in veiculos]


@router.get("/{veiculo_id}")
def buscar_veiculo(veiculo_id: str):
    veiculo = veiculo_repo_instance.buscar_por_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veiculo nao encontrado")
    return veiculo.to_dict()


def _sincronizar_veiculo_com_servico_vendas(veiculo_data: dict):
    try:
        httpx.post(
            f"{settings.SALES_SERVICE_URL}/veiculos/sync",
            json=veiculo_data,
            timeout=5.0,
        )
    except httpx.RequestError:
        pass
