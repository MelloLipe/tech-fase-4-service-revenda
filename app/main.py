from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.controllers.veiculo_controller import router as veiculo_router
from app.infrastructure.controllers.pagamento_controller import router as pagamento_router

app = FastAPI(
    title="Revenda Veiculos - Servico Principal",
    version="1.0.0",
    description="API principal para cadastro de veiculos e processamento de pagamentos",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(veiculo_router, prefix="/veiculos", tags=["Veiculos"])
app.include_router(pagamento_router, prefix="/pagamentos", tags=["Pagamentos"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "servico-principal"}
