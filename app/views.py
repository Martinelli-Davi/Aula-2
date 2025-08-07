from django.shortcuts import render, redirect
from .models import Produto
# Create your views here.

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

def criar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        estoque = request.POST.get('estoque')
        foto = request.FILES.get('foto')
        Produto.criar_produto(nome, int(estoque), foto)
        return redirect('index')
    return render(request, 'criar_produto.html')

def vender_produto(request, produto_id):
    Produto.vender_produto(produto_id, 1)  # Exemplo de venda de 1 unidade
    return redirect('index')