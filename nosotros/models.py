from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import URLValidator


# ──────────────────────────────────────────────────────────────────────────────
# 0) Página (singleton)
# ──────────────────────────────────────────────────────────────────────────────
class NosotrosPage(models.Model):
    # Solo 1 registro
    enabled = models.BooleanField(default=True)

    # Relación 1-1 a secciones
    header = models.OneToOneField(
        "InnerHeader", on_delete=models.SET_NULL, null=True, blank=True
    )
    about = models.OneToOneField(
        "AboutSection", on_delete=models.SET_NULL, null=True, blank=True
    )
    history = models.OneToOneField(
        "HistorySection", on_delete=models.SET_NULL, null=True, blank=True
    )
    ecoaldea = models.OneToOneField(
        "EcoAldeaSection", on_delete=models.SET_NULL, null=True, blank=True
    )
    # testimonios: a futuro

    class Meta:
        verbose_name = "1. Nuestro camino / About Us Page"
        verbose_name_plural = "1. Nuestro camino  / About Us Page"

    def __str__(self):
        return "Página Nosotros"


# ──────────────────────────────────────────────────────────────────────────────
# 1) Inner Header
# ──────────────────────────────────────────────────────────────────────────────
class InnerHeader(models.Model):
    title = models.CharField("Título", max_length=120, default="Nosotros")
    breadcrumb_label = models.CharField(
        "Breadcrumb actual", max_length=120, default="Nuestro camino"
    )
    background = models.ImageField(
        upload_to="nosotros/", help_text="Imagen de fondo del header"
    )

    class Meta:
        verbose_name = "1.1. Nuestro camino - Sección: Cabecera / Header Section"
        verbose_name_plural = "1.1. Nuestro camino - Sección: Cabecera / Header Section"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# 2) About + Video
# ──────────────────────────────────────────────────────────────────────────────
class AboutSection(models.Model):
    title = models.CharField(max_length=160, default="Chambalabamba, ecoaldea viva")
    lead = models.TextField("Intro (negrita)", blank=True)
    body = models.TextField("Párrafo", blank=True)
    cta_text = models.CharField(
        "Texto botón", max_length=80, blank=True, default="Contact Us"
    )
    cta_url = models.CharField("URL botón", max_length=300, blank=True)
    video_url = models.CharField(
        "URL de video (Vimeo/YouTube)",
        max_length=500,
        validators=[URLValidator()],
        blank=True,
    )

    class Meta:
        verbose_name = "1.2 Nuestro camino - Sección: Acerca + Video / About + Video"
        verbose_name_plural = (
            "1.2 Nuestro camino - Sección: Acerca + Video / About + Video"
        )

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# 3) Historia (imagen lateral + timeline)
# ──────────────────────────────────────────────────────────────────────────────
class HistorySection(models.Model):
    subtitle = models.CharField(
        "Subtítulo", max_length=120, default="About our History"
    )
    title = models.CharField("Título", max_length=120, default="Our Success Story")
    side_image = models.ImageField(upload_to="nosotros/", blank=True, null=True)

    class Meta:
        verbose_name = "1.3 Nuestro camino - Sección: Historia / History Section"
        verbose_name_plural = "1.3 Nuestro camino - Sección: Historia / History Section"

    def __str__(self):
        return self.title


class TimelinePeriod(models.Model):
    history = models.ForeignKey(
        HistorySection, on_delete=models.CASCADE, related_name="periods"
    )
    label = models.CharField("Rango de años", max_length=60)  # ej: "2000 - 2002"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Periodo (Timeline) / Timeline Period"
        verbose_name_plural = "Periodos (Timeline) / Timeline Periods"

    def __str__(self):
        return self.label


class TimelineItem(models.Model):
    period = models.ForeignKey(
        TimelinePeriod, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=120)
    body = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Caja de Timeline"
        verbose_name_plural = "Cajas de Timeline"

    def __str__(self):
        return f"{self.period.label} · {self.title}"


# ──────────────────────────────────────────────────────────────────────────────
# 4) EcoAldea (3 tarjetas)
# ──────────────────────────────────────────────────────────────────────────────
class EcoAldeaSection(models.Model):
    title = models.CharField(max_length=160, default="Sé parte de la Eco Aldea")

    class Meta:
        verbose_name = "1.4 Nuestro camino - Sección: EcoAldea / EcoVillage Section"
        verbose_name_plural = (
            "1.4 Nuestro camino - Sección: EcoAldea / EcoVillage Section"
        )

    def __str__(self):
        return self.title


class EcoAldeaCard(models.Model):
    section = models.ForeignKey(
        EcoAldeaSection, on_delete=models.CASCADE, related_name="cards"
    )
    icon = models.ImageField(
        upload_to="nosotros/", help_text="Icono ~60px de alto", blank=True, null=True
    )
    title = models.CharField(max_length=120)
    text = models.TextField()
    link_text = models.CharField("Texto del enlace", max_length=120, blank=True)
    link_url = models.CharField("URL del enlace", max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Tarjeta EcoAldea / EcoVillage Card"
        verbose_name_plural = "Tarjeta EcoAldea / EcoVillage Card"

    def __str__(self):
        return self.title

        # ───────────────────────────────────────────────
        # PILARES (Ecología, Economía, Bienestar, Sociocultural)
        # ───────────────────────────────────────────────


class BaseOrdenPublicado(models.Model):
    publicado = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["orden", "-creado"]


# --- HEADER -------------------------------------------------
class PageHeader(models.Model):
    title = models.CharField(max_length=120, default="Nosotros")
    breadcrumb_label = models.CharField(
        max_length=120, blank=True, help_text="Texto del breadcrumb nivel 2/3"
    )
    background = models.ImageField(upload_to="nosotros/headers/", blank=True, null=True)

    def __str__(self):
        return self.title


# --- PILAR PAGE (reutilizable: ecologia, economia, bienestar, sociocultural) ---
class PilarPage(models.Model):
    SLUG_CHOICES = [
        ("ecologia", "Ecología"),
        ("economia", "Economía comunitaria"),
        ("bienestar", "Bienestar integral"),
        ("sociocultural", "Sociocultural"),
    ]
    slug = models.SlugField(unique=True, choices=SLUG_CHOICES)
    header = models.OneToOneField(
        PageHeader, on_delete=models.SET_NULL, null=True, blank=True
    )
    hero_image = models.ImageField(
        upload_to="nosotros/pilares/hero/", blank=True, null=True
    )
    title = models.CharField(max_length=150, default="Pilar")
    # opcional: lead corto si lo necesitas más adelante
    lead = models.TextField(blank=True)

    project_placements = GenericRelation(
        "proyectos.ProjectPlacement", related_query_name="pilar_page"
    )

    class Meta:
        verbose_name = "2. Pilar"
        verbose_name_plural = "2. Pilares"

    def __str__(self):
        return f"{self.get_slug_display()}"


# --- BLOQUES DE TEXTO PRINCIPALES --------------------------
class PilarParagraph(BaseOrdenPublicado):
    page = models.ForeignKey(
        PilarPage, related_name="paragraphs", on_delete=models.CASCADE
    )
    body = models.TextField()

    def __str__(self):
        return f"Párrafo {self.orden} · {self.page}"


class PilarQuote(BaseOrdenPublicado):
    page = models.ForeignKey(PilarPage, related_name="quotes", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Cita {self.orden} · {self.page}"


# --- SIDEBAR ------------------------------------------------
class PilarSidebarWidget(BaseOrdenPublicado):
    page = models.ForeignKey(
        PilarPage, related_name="sidebar", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    text = models.TextField()

    def __str__(self):
        return f"Sidebar: {self.title} · {self.page}"


# ──────────────────────────────────────────────────────────────────────────────
# NOSOTROS: Secciones (Gobernanza, Principios y valores, Territorio)
# ──────────────────────────────────────────────────────────────────────────────
class TopicPage(models.Model):
    SLUG_CHOICES = [
        ("gobernanza", "Gobernanza"),
        ("principios_valores", "Principios y valores"),
        ("territorio", "Territorio"),
    ]
    slug = models.SlugField(unique=True, choices=SLUG_CHOICES)
    header = models.OneToOneField(
        PageHeader, on_delete=models.SET_NULL, null=True, blank=True
    )
    hero_image = models.ImageField(
        upload_to="nosotros/sections/hero/", blank=True, null=True
    )
    title = models.CharField(max_length=150, default="Sección")
    lead = models.TextField(blank=True)

    project_placements = GenericRelation(
        "proyectos.ProjectPlacement", related_query_name="topic_page"
    )

    class Meta:
        verbose_name = "Sección (Nosotros)"
        verbose_name_plural = "Secciones (Nosotros)"

    def __str__(self):
        return self.get_slug_display()


class TopicParagraph(BaseOrdenPublicado):
    page = models.ForeignKey(
        TopicPage, related_name="paragraphs", on_delete=models.CASCADE
    )
    body = models.TextField()

    def __str__(self):
        return f"Párrafo {self.orden} · {self.page}"


class TopicQuote(BaseOrdenPublicado):
    page = models.ForeignKey(TopicPage, related_name="quotes", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Cita {self.orden} · {self.page}"


class TopicSidebarWidget(BaseOrdenPublicado):
    page = models.ForeignKey(
        TopicPage, related_name="sidebar", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    text = models.TextField()

    def __str__(self):
        return f"Sidebar: {self.title} · {self.page}"


# === PROXIES ===
class GobernanzaPage(TopicPage):
    class Meta:
        proxy = True
        verbose_name = "3. Gobernanza"
        verbose_name_plural = "3. Gobernanza"


class PrincipiosValoresPage(TopicPage):
    class Meta:
        proxy = True
        verbose_name = "4. Principios y valores"
        verbose_name_plural = "4. Principios y valores"


class TerritorioPage(TopicPage):
    class Meta:
        proxy = True
        verbose_name = "5. Territorio"
        verbose_name_plural = "5. Territorio"
