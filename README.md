# Servico Principal - Cadastro de Veiculos

Microsservico principal responsavel pelo cadastro de veiculos para venda, edicao de dados e processamento de pagamentos via webhook. Faz parte da plataforma de revenda de veiculos automotores.

## Arquitetura

O projeto segue **Clean Architecture** com as seguintes camadas:

```
app/
├── config/          # Configuracoes da aplicacao
├── domain/
│   ├── entities/    # Entidades de dominio (Veiculo, Pagamento)
│   └── repositories/ # Interfaces dos repositorios (ABC)
├── application/
│   ├── dtos/        # Data Transfer Objects (Pydantic)
│   └── usecases/    # Casos de uso da aplicacao
└── infrastructure/
    ├── controllers/ # Endpoints FastAPI
    └── persistence/ # Implementacao dos repositorios (InMemory)
```

## Funcionalidades

- **Cadastrar veiculo para venda** - Marca, modelo, ano, cor, preco
- **Editar dados do veiculo** - Atualiza qualquer campo do veiculo
- **Webhook de pagamento** - Recebe notificacao de pagamento (PAGO ou CANCELADO)
- **Registrar pagamento** - Cria registro de pagamento para um veiculo vendido
- **Sincronizacao** - Envia dados de veiculos para o servico de vendas via HTTP

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | `/veiculos/` | Cadastra um novo veiculo para venda |
| PUT | `/veiculos/{id}` | Edita dados de um veiculo |
| GET | `/veiculos/` | Lista todos os veiculos |
| GET | `/veiculos/{id}` | Busca veiculo por ID |
| POST | `/pagamentos/webhook` | Webhook para processar pagamento |
| POST | `/pagamentos/registrar` | Registra um pagamento |
| GET | `/pagamentos/{codigo}` | Busca pagamento por codigo |
| GET | `/health` | Health check |

## Como usar localmente

### Pre-requisitos
- Python 3.11+
- pip

### Instalacao

```bash
pip install -r requirements.txt
```

### Executar

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estara disponivel em `http://localhost:8000`

Documentacao Swagger: `http://localhost:8000/docs`

### Com Docker

```bash
docker-compose up --build
```

## Como testar

```bash
pytest tests/ -v
```

## Fluxo completo (ponta-a-ponta)

1. **Cadastrar veiculo** (POST `/veiculos/`) - O veiculo e sincronizado automaticamente com o servico de vendas
2. **Listar veiculos a venda** (GET no servico de vendas `/veiculos/a-venda`)
3. **Comprar veiculo** (POST no servico de vendas `/veiculos/comprar`) - Gera codigo de pagamento
4. **Processar pagamento** (POST `/pagamentos/webhook`) - Marca como PAGO ou CANCELADO
5. **Listar veiculos vendidos** (GET no servico de vendas `/veiculos/vendidos`)

## Comunicacao entre servicos

Este servico se comunica com o **Servico de Vendas** (porta 8001) via HTTP:

- Ao cadastrar/editar um veiculo, sincroniza os dados com o servico de vendas
- Ao processar um webhook de pagamento, notifica o servico de vendas sobre o status

### Variavel de ambiente

```
SALES_SERVICE_URL=http://localhost:8001
```

## CI/CD

- **CI**: Testes automatizados em toda PR para `main`
- **CD**: Deploy automatizado ao fazer merge na branch `main`
