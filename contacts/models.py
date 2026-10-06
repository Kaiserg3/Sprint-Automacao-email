from django.conf import settings
from django.db import models


class Contato(models.Model):
    """Uma pessoa/RH de empresa para quem os emails de prospecção são enviados."""

    STATUS_CHOICES = [
        ("valido", "Válido"),
        ("invalido", "Inválido (bounce)"),
    ]

    # related_name="contatos" permite fazer usuario.contatos.all()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contatos"
    )
    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("Email")
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default="valido")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Envio(models.Model):
    """Um email enviado para um Contato. Cada Contato pode ter vários Envios (1:N)."""

    STATUS_CHOICES = [
        ("enviado", "Enviado"),
        ("pendente", "Pendente"),
        ("bounce", "Bounce (falhou)"),
    ]

    # on_delete=CASCADE: se o contato for excluído, os envios dele também são
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, related_name="envios")
    assunto = models.CharField("Assunto", max_length=200)
    corpo = models.TextField("Corpo do email")
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default="pendente")
    data_envio = models.DateTimeField("Data de envio", auto_now_add=True)

    def __str__(self):
        return f"{self.assunto} → {self.contato.nome}"
