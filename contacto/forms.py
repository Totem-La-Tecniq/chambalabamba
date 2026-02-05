from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Contacto


def validate_no_rude_words(value):
    rude_words = [
        "fuck",
        "shit",
        "damn",
        "hell",
        "bitch",
        "bastard",
        "idiot",
        "moron",
        "dumbass",
        "jerk",
        "retard",
        "porn",
        "sex",
        "blowjob",
        "dick",
        "pussy",
        "tits",
        "racist",
        "nazi",
        "hate",
        "kill",
        "die",
        "suicide",
        "crap",
        "ass",
        "whore",
        "slut",
        "motherf***er",
        "mierda",
        "joder",
        "coño",
        "puta",
        "cabrón",
        "gilipollas",
        "idiota",
        "imbécil",
        "pendejo",
        "pelotudo",
        "tonto",
        "sexo",
        "porno",
        "polla",
        "tetas",
        "verga",
        "follar",
        "odio",
        "matar",
        "morir",
        "nazi",
        "racista",
        "maldito",
        "asqueroso",
        "desgraciado",
    ]
    for word in rude_words:
        if word in value.lower():
            raise ValidationError(
                f"Por favor, evita el uso de palabras inapropiadas como '{word}'."
            )


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombres"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Correo Electrónico"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Teléfono"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Asunto"}
            ),
            "message": forms.Textarea(
                attrs={"class": "textarea-control", "placeholder": "Mensaje"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].validators.append(validate_no_rude_words)
        self.fields["email"].validators.append(validate_no_rude_words)
        self.fields["phone"].validators.append(
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos.",
            )
        )
        self.fields["phone"].validators.append(validate_no_rude_words)
        self.fields["subject"].validators.append(validate_no_rude_words)
        self.fields["message"].validators.append(validate_no_rude_words)
