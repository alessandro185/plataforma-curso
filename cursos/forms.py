from django import forms
from django.core.exceptions import ValidationError

from .models import Inscricao


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ("nome", "email", "telefone", "observacoes")
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone (opcional)",
            "observacoes": "Mensagem (opcional)",
        }
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Como devemos te chamar",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input",
                    "placeholder": "seu@email.com",
                    "autocomplete": "email",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "WhatsApp ou telefone",
                    "autocomplete": "tel",
                }
            ),
            "observacoes": forms.Textarea(
                attrs={
                    "class": "input input-area",
                    "rows": 4,
                    "placeholder": "Turma desejada, disponibilidade, dúvidas…",
                }
            ),
        }

    def __init__(self, *args, curso=None, **kwargs):
        self.curso = curso
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if self.curso is None:
            return email
        if Inscricao.objects.filter(curso=self.curso, email__iexact=email).exists():
            raise ValidationError(
                "Já existe uma inscrição com este e-mail neste curso. "
                "Se precisar alterar dados, fale com o suporte."
            )
        return email
