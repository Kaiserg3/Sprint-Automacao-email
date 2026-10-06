from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Contato, Envio
from .forms import ContatoForm, EnvioForm


# ---------------------------------------------------------------------------
# CRUD de Contato
# ---------------------------------------------------------------------------

@login_required
def contato_list(request):
    # Read: cada usuário só vê os próprios contatos
    contatos = Contato.objects.filter(usuario=request.user)
    return render(request, "contacts/contato_list.html", {"contatos": contatos})


@login_required
def contato_create(request):
    # Create
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            contato = form.save(commit=False)
            contato.usuario = request.user
            contato.save()
            messages.success(request, "Contato criado com sucesso!")
            return redirect("contato_list")
    else:
        form = ContatoForm()
    return render(request, "contacts/contato_form.html", {"form": form, "titulo": "Novo contato"})


@login_required
def contato_update(request, pk):
    # Update — get_object_or_404 com usuario=request.user impede editar contato de outra pessoa
    contato = get_object_or_404(Contato, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = ContatoForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            messages.success(request, "Contato atualizado com sucesso!")
            return redirect("contato_list")
    else:
        form = ContatoForm(instance=contato)
    return render(request, "contacts/contato_form.html", {"form": form, "titulo": "Editar contato"})


@login_required
def contato_delete(request, pk):
    # Delete
    contato = get_object_or_404(Contato, pk=pk, usuario=request.user)
    if request.method == "POST":
        contato.delete()  # os Envios desse contato são excluídos junto (CASCADE)
        messages.success(request, "Contato excluído.")
        return redirect("contato_list")
    return render(request, "contacts/contato_confirm_delete.html", {"contato": contato})


# ---------------------------------------------------------------------------
# CRUD de Envio (relacionado ao Contato)
# ---------------------------------------------------------------------------

@login_required
def envio_list(request):
    envios = Envio.objects.filter(contato__usuario=request.user).select_related("contato")
    return render(request, "contacts/envio_list.html", {"envios": envios})


@login_required
def envio_create(request):
    if request.method == "POST":
        form = EnvioForm(request.POST, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Envio registrado com sucesso!")
            return redirect("envio_list")
    else:
        form = EnvioForm(usuario=request.user)
    return render(request, "contacts/envio_form.html", {"form": form, "titulo": "Novo envio"})


@login_required
def envio_update(request, pk):
    envio = get_object_or_404(Envio, pk=pk, contato__usuario=request.user)
    if request.method == "POST":
        form = EnvioForm(request.POST, instance=envio, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Envio atualizado com sucesso!")
            return redirect("envio_list")
    else:
        form = EnvioForm(instance=envio, usuario=request.user)
    return render(request, "contacts/envio_form.html", {"form": form, "titulo": "Editar envio"})


@login_required
def envio_delete(request, pk):
    envio = get_object_or_404(Envio, pk=pk, contato__usuario=request.user)
    if request.method == "POST":
        envio.delete()
        messages.success(request, "Envio excluído.")
        return redirect("envio_list")
    return render(request, "contacts/envio_confirm_delete.html", {"envio": envio})
