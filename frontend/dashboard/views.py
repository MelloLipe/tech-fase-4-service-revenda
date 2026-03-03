import httpx
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


def _get(url, timeout=5.0):
    try:
        resp = httpx.get(url, timeout=timeout)
        return resp.json(), resp.status_code
    except httpx.ConnectError:
        return {"error": "Servico indisponivel"}, 503
    except Exception as e:
        return {"error": str(e)}, 500


def _post(url, json_data=None, timeout=5.0):
    try:
        resp = httpx.post(url, json=json_data, timeout=timeout)
        return resp.json(), resp.status_code
    except httpx.ConnectError:
        return {"error": "Servico indisponivel"}, 503
    except Exception as e:
        return {"error": str(e)}, 500


def _put(url, json_data=None, timeout=5.0):
    try:
        resp = httpx.put(url, json=json_data, timeout=timeout)
        return resp.json(), resp.status_code
    except httpx.ConnectError:
        return {"error": "Servico indisponivel"}, 503
    except Exception as e:
        return {"error": str(e)}, 500


def index(request):
    main_health, main_status = _get(f"{settings.MAIN_SERVICE_URL}/health")
    sales_health, sales_status = _get(f"{settings.SALES_SERVICE_URL}/health")

    veiculos_data, _ = _get(f"{settings.MAIN_SERVICE_URL}/veiculos/")
    veiculos = veiculos_data if isinstance(veiculos_data, list) else []

    a_venda_data, _ = _get(f"{settings.SALES_SERVICE_URL}/veiculos/a-venda")
    a_venda = a_venda_data if isinstance(a_venda_data, list) else []

    vendidos_data, _ = _get(f"{settings.SALES_SERVICE_URL}/veiculos/vendidos")
    vendidos = vendidos_data if isinstance(vendidos_data, list) else []

    return render(request, 'dashboard/index.html', {
        'main_online': main_status == 200,
        'sales_online': sales_status == 200,
        'veiculos': veiculos,
        'a_venda': a_venda,
        'vendidos': vendidos,
        'total_veiculos': len(veiculos),
        'total_a_venda': len(a_venda),
        'total_vendidos': len(vendidos),
    })


def cadastrar_veiculo(request):
    if request.method == 'POST':
        payload = {
            "marca": request.POST.get("marca", ""),
            "modelo": request.POST.get("modelo", ""),
            "ano": int(request.POST.get("ano", 0)),
            "cor": request.POST.get("cor", ""),
            "preco": float(request.POST.get("preco", 0)),
        }
        data, status = _post(f"{settings.MAIN_SERVICE_URL}/veiculos/", payload)
        if status in (200, 201):
            messages.success(request, f"Veiculo cadastrado com sucesso! ID: {data.get('id', '')}")
            return redirect('index')
        else:
            messages.error(request, f"Erro ao cadastrar: {data}")

    return render(request, 'dashboard/cadastrar.html')


def editar_veiculo(request, veiculo_id):
    if request.method == 'POST':
        payload = {}
        for field in ['marca', 'modelo', 'ano', 'cor', 'preco']:
            value = request.POST.get(field)
            if value:
                if field == 'ano':
                    payload[field] = int(value)
                elif field == 'preco':
                    payload[field] = float(value)
                else:
                    payload[field] = value

        data, status = _put(f"{settings.MAIN_SERVICE_URL}/veiculos/{veiculo_id}", payload)
        if status == 200:
            messages.success(request, "Veiculo atualizado com sucesso!")
            return redirect('index')
        else:
            messages.error(request, f"Erro ao editar: {data}")

    veiculo_data, status = _get(f"{settings.MAIN_SERVICE_URL}/veiculos/{veiculo_id}")
    if status != 200:
        messages.error(request, "Veiculo nao encontrado")
        return redirect('index')

    return render(request, 'dashboard/editar.html', {'veiculo': veiculo_data})


def veiculos_a_venda(request):
    data, status = _get(f"{settings.SALES_SERVICE_URL}/veiculos/a-venda")
    veiculos = data if isinstance(data, list) else []
    return render(request, 'dashboard/a_venda.html', {'veiculos': veiculos})


def veiculos_vendidos(request):
    data, status = _get(f"{settings.SALES_SERVICE_URL}/veiculos/vendidos")
    veiculos = data if isinstance(data, list) else []
    return render(request, 'dashboard/vendidos.html', {'veiculos': veiculos})


def comprar_veiculo(request):
    if request.method == 'POST':
        payload = {
            "veiculo_id": request.POST.get("veiculo_id", ""),
            "cpf_comprador": request.POST.get("cpf_comprador", ""),
            "data_venda": request.POST.get("data_venda", ""),
        }
        data, status = _post(f"{settings.SALES_SERVICE_URL}/veiculos/comprar", payload)
        if status == 200:
            codigo = data.get("codigo_pagamento", "N/A")
            messages.success(request, f"Compra realizada! Codigo de pagamento: {codigo}")
            return redirect('index')
        else:
            error_detail = data.get("detail", data.get("error", str(data)))
            messages.error(request, f"Erro na compra: {error_detail}")

    a_venda_data, _ = _get(f"{settings.SALES_SERVICE_URL}/veiculos/a-venda")
    veiculos = a_venda_data if isinstance(a_venda_data, list) else []
    return render(request, 'dashboard/comprar.html', {'veiculos': veiculos})


def webhook_pagamento(request):
    if request.method == 'POST':
        payload = {
            "codigo_pagamento": request.POST.get("codigo_pagamento", ""),
            "status": request.POST.get("status", "PAGO"),
        }
        data, status = _post(f"{settings.MAIN_SERVICE_URL}/pagamentos/webhook", payload)
        if status == 200:
            messages.success(request, f"Webhook processado! Status: {data.get('status', '')}")
            return redirect('index')
        else:
            error_detail = data.get("detail", data.get("error", str(data)))
            messages.error(request, f"Erro no webhook: {error_detail}")

    return render(request, 'dashboard/webhook.html')


def health_check(request):
    main_data, main_status = _get(f"{settings.MAIN_SERVICE_URL}/health")
    sales_data, sales_status = _get(f"{settings.SALES_SERVICE_URL}/health")
    return render(request, 'dashboard/health.html', {
        'main_data': main_data,
        'main_status': main_status,
        'sales_data': sales_data,
        'sales_status': sales_status,
    })
