from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.index, name='index'),
    path('veiculos/cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculos/<str:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculos/a-venda/', views.veiculos_a_venda, name='veiculos_a_venda'),
    path('veiculos/vendidos/', views.veiculos_vendidos, name='veiculos_vendidos'),
    path('veiculos/comprar/', views.comprar_veiculo, name='comprar_veiculo'),
    path('pagamentos/webhook/', views.webhook_pagamento, name='webhook_pagamento'),
    path('health/', views.health_check, name='health_check'),
]
