from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """Formulário de cadastro: pede usuário, email e senha (com confirmação)."""

    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar senha")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "Usuário", "email": "Email"}

    def clean_username(self):
        # Garante que não existe outro usuário com o mesmo nome (erro tratado).
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Esse nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe uma conta com esse email.")
        return email

    def clean(self):
        # Validação cruzada entre dois campos: só dá para checar em "clean", não em "clean_<campo>".
        cleaned = super().clean()
        senha = cleaned.get("senha")
        confirmar = cleaned.get("confirmar_senha")
        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError("As senhas não coincidem.")
        if senha and len(senha) < 8:
            raise forms.ValidationError("A senha precisa ter pelo menos 8 caracteres.")
        return cleaned

    def save(self, commit=True):
        # set_password faz o hash da senha; nunca salvar senha em texto puro.
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"])
        if commit:
            user.save()
        return user
