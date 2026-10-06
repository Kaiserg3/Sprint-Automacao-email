from django import forms
from .models import Contato, Envio


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["nome", "email", "status"]


class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ["contato", "assunto", "corpo", "status"]

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra no campo "contato" só os contatos do usuário logado,
        # para um usuário não conseguir registrar envio para contato de outro.
        if usuario is not None:
            self.fields["contato"].queryset = Contato.objects.filter(usuario=usuario)
