from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm


def register_view(request):
    """Issue: Registro de usuário."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # já entra logado após o cadastro
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("dashboard")
        # form inválido: os erros ficam em form.errors e aparecem no template
        messages.error(request, "Corrija os erros abaixo para continuar.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Issue: Login com tratamento de sucesso e erro."""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.username}!")
            return redirect("dashboard")

        # authenticate() retorna None tanto para usuário inexistente quanto senha errada
        messages.error(request, "Usuário ou senha incorretos.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    """Issue: Proteção de rotas e sessão."""
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("login")


@login_required
def dashboard_view(request):
    # Página de exemplo só acessível a quem está autenticado (login_required cuida disso).
    return render(request, "accounts/dashboard.html")
