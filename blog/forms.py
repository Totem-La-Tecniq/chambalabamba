# blog/forms.py
from django import forms
from django.utils.text import slugify
from .models import BlogComment, BlogPost
import bleach  # <-- nuevo
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Configura qué HTML permites en cuerpo_html (ajústalo a tu gusto)
ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "a",
    "h2",
    "h3",
    "h4",
    "blockquote",
    "img",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto", "data"]


class BlogCommentForm(forms.ModelForm):
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = BlogComment
        fields = ("parent", "nombre", "email", "website", "cuerpo", "hp")
        widgets = {
            "parent": forms.HiddenInput(),
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (opcional)"}),
            "website": forms.URLInput(attrs={"placeholder": "Sitio (opcional)"}),
            "cuerpo": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Escribe tu comentario…"}
            ),
        }

    def clean_hp(self):
        v = self.cleaned_data.get("hp")
        if v:
            raise forms.ValidationError("Error de validación.")
        return v


class BlogPostForm(forms.ModelForm):
    cuerpo_html = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = BlogPost
        fields = [
            "titulo",
            "resumen",
            "cuerpo_html",
            "portada",
            "categoria",
            "tags",
            "tipo",
            "video_url",
            "audio_url",
            "enlace_externo",
            "publicado",
            "fecha_publicacion",
        ]
        widgets = {
            "resumen": forms.Textarea(attrs={"rows": 3}),
            "fecha_publicacion": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 QUITA EL CHECKBOX CLEAR (pero deja el campo portada)
        self.fields["portada"].widget = forms.FileInput()

    # --- NUEVO: sanea HTML permitido ---
    def clean_cuerpo_html(self):
        html = self.cleaned_data.get("cuerpo_html") or ""
        cleaned = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
        )
        # linkify (auto-<a>) si pega URLs planas
        cleaned = bleach.linkify(cleaned)
        return cleaned

    # --- NUEVO: valida tamaño/formatos de portada ---
    def clean_portada(self):
        img = self.cleaned_data.get("portada")
        if img:
            if img.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("La portada no debe superar 2MB.")
            if getattr(img, "content_type", "") not in {
                "image/jpeg",
                "image/png",
                "image/webp",
            }:
                raise forms.ValidationError("Formato no soportado (usa JPG/PNG/WEBP).")
        return img

    def clean(self):
        data = super().clean()
        # Si marcan publicado y no hay fecha, la pondremos en la vista (mantengo tu lógica)
        return data

    def generate_unique_slug(self, base):
        base = slugify(base)[:200] or "post"
        cand = base
        i = 1
        from .models import BlogPost

        while BlogPost.objects.filter(slug=cand).exists():
            cand = f"{base}-{i}"
            i += 1
        return cand
