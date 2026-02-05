# apps/estancias/models.py
from django.db import models
from django.utils.text import slugify
from inicio.models import BaseOrdenPublicado  # reutiliza tu base
from django.db.models.functions import Now

# --- Header + Página (patrón similar a 'Nosotros') ---


class EstanciasIntro(models.Model):
    page = models.OneToOneField(
        "ParticipaPage", on_delete=models.CASCADE, related_name="intro"
    )
    title = models.CharField(
        max_length=160, default="¡Vive Eco-Centro Chambalabamba: Elige tu estancia!"
    )
    body_html = models.TextField(
        blank=True,
        default=(
            "Tu lugar de descanso en la ecoaldea. Hospédate con nosotros y disfruta de ritmos lentos y amaneceres serenos. "
            "Un alquiler con sentido: comodidad simple, naturaleza y quietud interior."
        ),
    )
    quote_text = models.CharField(
        max_length=300,
        blank=True,
        default='"El conocimiento compartido se multiplica, la experiencia vivida se transforma en sabiduría"',
    )
    bg_color = models.CharField(max_length=20, default="#f8f9fa")
    margin_top_px = models.PositiveIntegerField(default=40)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Bloque intro Estancias"
        verbose_name_plural = "Bloque intro Estancias"

    def __str__(self):
        return self.title


class ParticipaHeader(models.Model):
    title = models.CharField("Título", max_length=120, default="Participa")
    breadcrumb_label = models.CharField(
        "Breadcrumb actual", max_length=120, default="Estancias"
    )
    background = models.ImageField(
        upload_to="participa/headers/", blank=True, null=True
    )

    class Meta:
        verbose_name = "5) Sección: Header (Participa)"
        verbose_name_plural = "5) Sección: Header (Participa)"

    def __str__(self):
        return self.title


class ParticipaPage(models.Model):
    enabled = models.BooleanField(default=True)
    header = models.OneToOneField(
        ParticipaHeader, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "3) Página: Galeria Estancias"
        verbose_name_plural = "3) Página: Participa/Estancias"

    def __str__(self):
        return "Página Participa"


#####################ESTANCIAS###################


class Estancia(BaseOrdenPublicado):
    SECCIONES = [
        ("participa_estancias", "Participa – Estancias"),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    seccion = models.CharField(
        max_length=50, choices=SECCIONES, default="participa_estancias"
    )
    resumen = models.TextField(blank=True)  # para el grid
    descripcion = models.TextField(blank=True)  # para el detalle
    tipo = models.CharField(max_length=120, blank=True)  # p.ej. "Casa de madera"
    lugar = models.CharField(
        max_length=200, blank=True, default="Ecocentro Chambalabamba"
    )
    portada = models.ImageField(upload_to="estancias/portadas/", blank=True)
    alt_portada = models.CharField(max_length=200, blank=True)

    # Precios opcionales
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_tachado = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )

    # Contacto opcional (para botón WhatsApp del detalle)
    phone_whatsapp = models.CharField(
        max_length=32,
        blank=True,
        help_text="Solo números con código de país, ej: 5939XXXXXXX",
    )

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "3) Galeria Estancias"
        verbose_name_plural = "3) Galeria Estancias"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class EstanciaFoto(BaseOrdenPublicado):
    estancia = models.ForeignKey(
        Estancia, on_delete=models.CASCADE, related_name="fotos"
    )
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="estancias/fotos/")
    alt = models.CharField(max_length=200, blank=True)

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Foto de estancia"
        verbose_name_plural = "Fotos de estancias"

    def __str__(self):
        base = self.titulo or self.alt or self.imagen.name
        return f"{self.estancia.titulo} – {base}"


class EstanciaSpec(models.Model):
    """Pares clave/valor para 'Información adicional' del detalle."""

    estancia = models.ForeignKey(
        Estancia, on_delete=models.CASCADE, related_name="specs"
    )
    orden = models.PositiveIntegerField(default=0)
    clave = models.CharField(max_length=120)  # ej. "Capacidad"
    valor = models.TextField()  # ej. "1–2 personas"

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Especificación"
        verbose_name_plural = "Especificaciones"

    def __str__(self):
        return f"{self.clave}: {self.valor[:40]}"


class InstaGallery(BaseOrdenPublicado):
    SECCIONES = [
        ("participa_instagram", "Participa – Instagram"),
        ("home_instagram", "Home – Instagram"),  # por si luego lo usas
    ]
    titulo = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    seccion = models.CharField(
        max_length=40, choices=SECCIONES, default="participa_instagram"
    )

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Galería Instagram"
        verbose_name_plural = "Galerías Instagram"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo or self.seccion)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or self.seccion


class InstaItem(BaseOrdenPublicado):
    galeria = models.ForeignKey(
        InstaGallery, on_delete=models.CASCADE, related_name="items"
    )
    titulo = models.CharField(max_length=120, blank=True)
    imagen = models.ImageField(upload_to="participa/instagram/")
    alt = models.CharField(max_length=160, blank=True)
    enlace = models.URLField(blank=True)  # link del icono (o deja vacío para "#")

    class Meta(BaseOrdenPublicado.Meta):
        verbose_name = "Foto Instagram"
        verbose_name_plural = "Fotos Instagram"

    def __str__(self):
        return self.titulo or self.alt or self.imagen.name


# LOS MODELOS PARA PARTICIPA voluntariado BASADO EN EL TEMPLATE

# participa/models.py


class ContentBlock(models.Model):
    """Bloques reutilizables: título + HTML + imagen opcional."""

    title = models.CharField(max_length=150)
    body_html = models.TextField(blank=True)
    image = models.ImageField(upload_to="participa/blocks/", blank=True, null=True)

    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True, db_default=Now())
    actualizado = models.DateTimeField(auto_now=True, db_default=Now())

    class Meta:
        ordering = ("orden", "title")
        app_label = "participa"
        verbose_name = "4) Bloques de contenido "
        verbose_name_plural = "4) Bloques de contenido"

    def __str__(self):
        return self.title


class VoluntariadoPage(models.Model):
    """Singleton editable para la página de Voluntariado."""

    titulo = models.CharField(
        max_length=150, default="Voluntariado: nuestra filosofía y cómo involucrarte"
    )
    subtitulo = models.CharField(max_length=200, blank=True)

    # Cabecera + miniatura del artículo
    background = models.ImageField(
        upload_to="participa/voluntariado/hero/", blank=True, null=True
    )
    thumb = models.ImageField(
        upload_to="participa/voluntariado/thumb/", blank=True, null=True
    )

    # Bloques administrables (estilo 'Nosotros' con selects y botón de +)
    about_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vol_about",
    )
    ambiente_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vol_ambiente",
    )

    # Texto libre opcional (fallback)
    intro_html = models.TextField(blank=True)

    # Quote
    quote_text = models.CharField(max_length=300, blank=True)
    quote_author = models.CharField(max_length=120, blank=True)

    # Instagram
    instagram_embed_url = models.URLField(
        blank=True, help_text="Permalink canónico del Reel/Post"
    )

    # CTA de contacto (administrable)
    contact_cta_label = models.CharField(
        max_length=80, blank=True, default="Proponer cooperación"
    )
    contact_cta_url = models.URLField(
        blank=True,
        help_text="URL absoluta o relativa; si vacío, usa {% url 'contacto:contacto' %}",
    )

    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "1) Página de Voluntariado"
        verbose_name_plural = "1) Página de Voluntariado"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ProyectoVoluntariado(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    link = models.URLField(blank=True)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ("orden", "nombre")
        verbose_name = "2) Proyectos de voluntariado"
        verbose_name_plural = "2) Proyectos de voluntariado"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)[:50]
        super().save(*args, **kwargs)


# ------------------------------
# 1) Página (singleton) Visitas guiadas
# ------------------------------


class GuidedVisitsPage(models.Model):
    """Página principal de la sección 'Visitas guiadas' (singleton)."""

    publicado = models.BooleanField(default=True)

    # Cabecera
    titulo = models.CharField(
        max_length=160,
        default="Visitas guiadas: conoce Chambalabamba en comunidad",
    )
    subtitulo = models.CharField(
        max_length=200,
        blank=True,
        help_text="Frase bajo el título (opcional).",
    )
    background = models.ImageField(
        upload_to="participa/visitas/hero/",
        blank=True,
        null=True,
        help_text="Imagen grande de cabecera (si usas header dinámico).",
    )
    thumb = models.ImageField(
        upload_to="participa/visitas/thumb/",
        blank=True,
        null=True,
        help_text="Imagen usada dentro del contenido (fallback si no hay hero).",
    )

    # Bloques administrables (estilo 'Nosotros')
    about_block = models.ForeignKey(
        ContentBlock,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="visitas_about",
    )
    info_block = models.ForeignKey(
        ContentBlock,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="visitas_info",
        help_text="Información práctica/FAQ/indicaciones (opcional).",
    )

    # Fallback / extras
    intro_html = models.TextField(blank=True)
    quote_text = models.CharField(max_length=300, blank=True)
    quote_author = models.CharField(max_length=120, blank=True)
    instagram_embed_url = models.URLField(blank=True)

    # CTA de contacto
    contact_cta_label = models.CharField(
        max_length=80, blank=True, default="Consultar disponibilidad"
    )
    contact_cta_url = models.URLField(
        blank=True,
        help_text="Si lo dejas vacío, puedes usar una URL relativa en la plantilla.",
    )

    creado = models.DateTimeField(auto_now_add=True, db_default=Now())
    actualizado = models.DateTimeField(auto_now=True, db_default=Now())

    class Meta:
        verbose_name = "1) Página de Visitas guiadas"
        verbose_name_plural = "1) Página de Visitas guiadas"

    def __str__(self):
        return self.titulo

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
