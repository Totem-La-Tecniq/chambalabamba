from django.db import models
from django.utils.text import slugify


class Festival(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    date = models.CharField(max_length=200, verbose_name="Fecha")
    time = models.CharField(max_length=200, verbose_name="Hora")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.ImageField(
        upload_to="festivales", verbose_name="Imagen", null=True, blank=True
    )
    flyer = models.ImageField(
        upload_to="festivales/flyers", verbose_name="Flyer", null=True, blank=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        blank=True,
        help_text="Dejar en blanco para autogenerar.",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "1.3 Sección: Lista de Festivales"
        verbose_name_plural = "1.3 Sección: Lista de Festivales"


class FestivalImage(models.Model):
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(
        upload_to="festivales/gallery/", verbose_name="Imagen de Galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de Galería del Festival"
        verbose_name_plural = "Imágenes de Galería del Festival"

    def __str__(self):
        return self.alt_text or f"Imagen para {self.festival.name}"


class TallerDetail(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    schedule = models.CharField(max_length=200, verbose_name="Horario")
    place = models.CharField(max_length=200, verbose_name="Lugar")
    image = models.ImageField(upload_to="talleres", verbose_name="Imagen")
    flyer = models.ImageField(
        upload_to="talleres/flyers", verbose_name="Flyer", null=True, blank=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        blank=True,
        help_text="Dejar en blanco para autogenerar.",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "2.3 Sección: Lista de Talleres"
        verbose_name_plural = "2.3 Sección: Lista de Talleres"
        db_table = "eventos_taller"


class TallerImage(models.Model):
    taller = models.ForeignKey(
        TallerDetail, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(
        upload_to="talleres/gallery/", verbose_name="Imagen de Galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de Galería del Taller"
        verbose_name_plural = "Imágenes de Galería del Taller"

    def __str__(self):
        return self.alt_text or f"Imagen para {self.taller.name}"


# ──────────────────────────────────────────────────────────────────────────────
# Página de Talleres
# ──────────────────────────────────────────────────────────────────────────────


class TalleresPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "TalleresHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "TalleresIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )

    class Meta:
        verbose_name = "2. Página: Talleres"
        verbose_name_plural = "2. Página: Talleres"

    def __str__(self):
        return "Página de Talleres"


class TalleresHeader(models.Model):
    title = models.CharField(max_length=120, default="Talleres", verbose_name="Título")
    breadcrumb_label = models.CharField(
        max_length=120, default="Talleres", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/", help_text="Imagen de fondo del header"
    )

    class Meta:
        verbose_name = "2.1 Sección: Header de Talleres"
        verbose_name_plural = "2.1 Sección: Header de Talleres"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# Página de Escuela
# ──────────────────────────────────────────────────────────────────────────────


class EscuelaPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "EscuelaHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "EscuelaIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )
    sidebar = models.OneToOneField(
        "EscuelaSidebar",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sidebar",
    )

    class Meta:
        verbose_name = "4. Página: Escuela"
        verbose_name_plural = "4. Página: Escuela"

    def __str__(self):
        return "Página de Escuela"


class EscuelaHeader(models.Model):
    title = models.CharField(
        max_length=120, default="Escuela Viva", verbose_name="Título"
    )
    breadcrumb_label = models.CharField(
        max_length=120, default="Escuela", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen de fondo del header",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "4.1 Sección: Header de Escuela"
        verbose_name_plural = "4.1 Sección: Header de Escuela"

    def __str__(self):
        return self.title


class EscuelaIntroSection(models.Model):
    main_image = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen principal de la sección de introducción",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=160,
        default="Conoce la escuela, nuestra filosofía e infraestructura",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    gallery_title = models.CharField(
        max_length=160, default="Nuestro dia a dia", verbose_name="Título de la galería"
    )

    class Meta:
        verbose_name = "4.2 Sección: Introducción de Escuela"
        verbose_name_plural = "4.2 Sección: Introducción de Escuela"

    def __str__(self):
        return self.title


class EscuelaGalleryImage(models.Model):
    section = models.ForeignKey(
        EscuelaIntroSection, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(
        upload_to="eventos/gallery/", help_text="Imagen para la galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de la Galería de Escuela"
        verbose_name_plural = "Imágenes de la Galería de Escuela"

    def __str__(self):
        return self.alt_text or f"Imagen {self.id}"


class EscuelaSidebar(models.Model):
    title = models.CharField(
        max_length=160,
        default="Un ambiente diseñado para el desarrollo infantil",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")
    instagram_url = models.URLField(
        blank=True, verbose_name="URL del post de Instagram"
    )
    projects_title = models.CharField(
        max_length=160,
        default="Proyectos de la escuela en curso",
        verbose_name="Título de los proyectos",
    )

    class Meta:
        verbose_name = "4.3 Sección: Sidebar de Escuela"
        verbose_name_plural = "4.3 Sección: Sidebar de Escuela"

    def __str__(self):
        return self.title


class EscuelaProject(models.Model):
    sidebar = models.ForeignKey(
        EscuelaSidebar, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=120, verbose_name="Nombre del proyecto")
    url = models.URLField(blank=True, verbose_name="URL del proyecto")

    class Meta:
        verbose_name = "Proyecto de Escuela"
        verbose_name_plural = "Proyectos de Escuela"

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────────────────────────────────────
# Página de Artes
# ──────────────────────────────────────────────────────────────────────────────


class ArtesPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "ArtesHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "ArtesIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )
    diversity = models.OneToOneField(
        "ArtesDiversitySection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Diversidad",
    )
    gallery = models.OneToOneField(
        "ArtesGallerySection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Galería",
    )

    class Meta:
        verbose_name = "3. Página: Artes"
        verbose_name_plural = "3. Página: Artes"

    def __str__(self):
        return "Página de Artes"


class ArtesHeader(models.Model):
    title = models.CharField(max_length=120, default="Artes", verbose_name="Título")
    breadcrumb_label = models.CharField(
        max_length=120, default="Artes", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen de fondo del header",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "3.1 Sección: Header de Artes"
        verbose_name_plural = "3.1 Sección: Header de Artes"

    def __str__(self):
        return self.title


class ArtesIntroSection(models.Model):
    main_image = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen principal de la sección de introducción",
        null=True,
        blank=True,
    )
    subtitle = models.CharField(
        max_length=160,
        default="En Chambalabamba el arte se vive",
        verbose_name="Subtítulo",
    )
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    sidebar_title = models.CharField(
        max_length=160,
        default="El arte no se detiene en Chambalabamba",
        verbose_name="Título del sidebar",
    )
    sidebar_paragraph1 = models.TextField(
        blank=True, verbose_name="Párrafo 1 del sidebar"
    )
    sidebar_paragraph2 = models.TextField(
        blank=True, verbose_name="Párrafo 2 del sidebar"
    )

    class Meta:
        verbose_name = "3.2 Sección: Introducción de Artes"
        verbose_name_plural = "3.2 Sección: Introducción de Artes"

    def __str__(self):
        return self.subtitle


class ArtesDiversitySection(models.Model):
    title = models.CharField(
        max_length=160,
        default="Danza, teatro, música y DIVERSIDAD",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "3.3 Sección: Diversidad de Artes"
        verbose_name_plural = "3.3 Sección: Diversidad de Artes"

    def __str__(self):
        return self.title


class Arte(models.Model):
    page = models.ForeignKey(
        ArtesDiversitySection, on_delete=models.CASCADE, related_name="artes"
    )
    title = models.CharField(max_length=120, verbose_name="Título")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    image = models.ImageField(
        upload_to="eventos/", help_text="Imagen del arte", null=True, blank=True
    )

    class Meta:
        verbose_name = "Arte"
        verbose_name_plural = "Artes"

    def __str__(self):
        return self.title


class ArtesGallerySection(models.Model):
    title = models.CharField(
        max_length=160, default="Momentos de creación colectiva", verbose_name="Título"
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "3.4 Sección: Galería de Artes"
        verbose_name_plural = "3.4 Sección: Galería de Artes"

    def __str__(self):
        return self.title


class ArtesGalleryImage(models.Model):
    section = models.ForeignKey(
        ArtesGallerySection, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="eventos/gallery/", help_text="Imagen para la galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de la Galería"
        verbose_name_plural = "Imágenes de la Galería"

    def __str__(self):
        return self.alt_text or f"Imagen {self.id}"


# ──────────────────────────────────────────────────────────────────────────────
# Página de Festivales
# ──────────────────────────────────────────────────────────────────────────────


class FestivalesPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "FestivalesHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "FestivalesIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )

    class Meta:
        verbose_name = "1. Página: Festivales"
        verbose_name_plural = "1. Página: Festivales"

    def __str__(self):
        return "Página de Festivales"


class FestivalesHeader(models.Model):
    title = models.CharField(
        max_length=120, default="Festivales", verbose_name="Título"
    )
    breadcrumb_label = models.CharField(
        max_length=120, default="Festivales", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/", help_text="Imagen de fondo del header"
    )

    class Meta:
        verbose_name = "1.1 Sección: Header de Festivales"
        verbose_name_plural = "1.1 Sección: Header de Festivales"

    def __str__(self):
        return self.title


class FestivalesIntroSection(models.Model):
    title = models.CharField(
        max_length=160, default="¡Celebra con nosotros!", verbose_name="Título"
    )
    paragraph1 = models.TextField(blank=True, verbose_name="Párrafo 1")
    paragraph2 = models.TextField(blank=True, verbose_name="Párrafo 2")
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    cta_text = models.CharField(
        max_length=80,
        blank=True,
        default="Ver todos los festivales",
        verbose_name="Texto del botón",
    )
    cta_url = models.CharField(
        max_length=300,
        blank=True,
        default="#festivales-grid",
        verbose_name="URL del botón",
    )

    class Meta:
        verbose_name = "1.2 Sección: Introducción de Festivales"
        verbose_name_plural = "1.2 Sección: Introducción de Festivales"

    def __str__(self):
        return self.title


class TalleresIntroSection(models.Model):
    title = models.CharField(
        max_length=160,
        default="¡Únete a nuestros talleres transformadores!",
        verbose_name="Título",
    )
    paragraph1 = models.TextField(blank=True, verbose_name="Párrafo 1")
    paragraph2 = models.TextField(blank=True, verbose_name="Párrafo 2")
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    cta_text = models.CharField(
        max_length=80,
        blank=True,
        default="Ver todos los talleres",
        verbose_name="Texto del botón",
    )
    cta_url = models.CharField(
        max_length=300,
        blank=True,
        default="#talleres-grid",
        verbose_name="URL del botón",
    )

    class Meta:
        verbose_name = "2.2 Sección: Introducción de Talleres"
        verbose_name_plural = "2.2 Sección: Introducción de Talleres"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────────────────────────────────────
# Página de Retiros
# ──────────────────────────────────────────────────────────────────────────────


class RetirosPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "RetirosHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "RetirosIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )
    types_section = models.OneToOneField(
        "RetirosTypesSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Tipos de Retiros",
    )
    activities_section = models.OneToOneField(
        "RetirosActivitiesSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Actividades",
    )
    second_quote = models.TextField(blank=True, verbose_name="Segunda Cita")
    gallery_section = models.OneToOneField(
        "RetirosGallerySection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Galería",
    )
    testimonial_section = models.OneToOneField(
        "RetirosTestimonialSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Testimonios",
    )

    class Meta:
        verbose_name = "5. Página: Retiros"
        verbose_name_plural = "5. Página: Retiros"

    def __str__(self):
        return "Página de Retiros"


class RetirosHeader(models.Model):
    title = models.CharField(max_length=120, default="Retiros", verbose_name="Título")
    breadcrumb_label = models.CharField(
        max_length=120, default="Retiros", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen de fondo del header",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "5.1 Sección: Header de Retiros"
        verbose_name_plural = "5.1 Sección: Header de Retiros"

    def __str__(self):
        return self.title


class RetirosIntroSection(models.Model):
    main_image = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen principal de la sección de introducción",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=160,
        default="Descubre y conecta con tu esencia",
        verbose_name="Título",
    )
    quote = models.CharField(max_length=255, blank=True, verbose_name="Cita")
    sidebar_title = models.CharField(
        max_length=160,
        default="Un viaje hacia tu interior",
        verbose_name="Título del sidebar",
    )
    sidebar_paragraph1 = models.TextField(
        blank=True, verbose_name="Párrafo 1 del sidebar"
    )
    sidebar_paragraph2 = models.TextField(
        blank=True, verbose_name="Párrafo 2 del sidebar"
    )
    sidebar_paragraph3 = models.TextField(
        blank=True, verbose_name="Párrafo 3 del sidebar"
    )

    class Meta:
        verbose_name = "5.2 Sección: Introducción de Retiros"
        verbose_name_plural = "5.2 Sección: Introducción de Retiros"

    def __str__(self):
        return self.title


class RetirosTypesSection(models.Model):
    title = models.CharField(
        max_length=160, default="Modalidades de transformación", verbose_name="Título"
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "5.3 Sección: Tipos de Retiros"
        verbose_name_plural = "5.3 Sección: Tipos de Retiros"

    def __str__(self):
        return self.title


class RetiroType(models.Model):
    section = models.ForeignKey(
        RetirosTypesSection, on_delete=models.CASCADE, related_name="types"
    )
    image = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen del tipo de retiro",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=120, verbose_name="Título")
    description = models.CharField(max_length=255, verbose_name="Descripción")

    class Meta:
        verbose_name = "Tipo de Retiro"
        verbose_name_plural = "Tipos de Retiros"

    def __str__(self):
        return self.title


class RetirosActivitiesSection(models.Model):
    title = models.CharField(
        max_length=160, default="Prácticas y experiencias", verbose_name="Título"
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "5.4 Sección: Actividades de Retiros"
        verbose_name_plural = "5.4 Sección: Actividades de Retiros"

    def __str__(self):
        return self.title


class RetiroActivity(models.Model):
    section = models.ForeignKey(
        RetirosActivitiesSection, on_delete=models.CASCADE, related_name="activities"
    )
    title = models.CharField(max_length=120, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "Actividad de Retiro"
        verbose_name_plural = "Actividades de Retiro"

    def __str__(self):
        return self.title


class RetirosGallerySection(models.Model):
    title = models.CharField(
        max_length=160,
        default="Espacios sagrados de transformación",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "5.5 Sección: Galería de Retiros"
        verbose_name_plural = "5.5 Sección: Galería de Retiros"

    def __str__(self):
        return self.title


class RetirosGalleryImage(models.Model):
    section = models.ForeignKey(
        RetirosGallerySection, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="eventos/gallery/", help_text="Imagen para la galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de la Galería de Retiros"
        verbose_name_plural = "Imágenes de la Galería de Retiros"

    def __str__(self):
        return self.alt_text or f"Imagen {self.id}"


class RetirosTestimonialSection(models.Model):
    title = models.CharField(
        max_length=160, default="Voces de transformación", verbose_name="Título"
    )

    class Meta:
        verbose_name = "5.6 Sección: Testimonios de Retiros"
        verbose_name_plural = "5.6 Sección: Testimonios de Retiros"

    def __str__(self):
        return self.title


class RetiroTestimonial(models.Model):
    section = models.ForeignKey(
        RetirosTestimonialSection, on_delete=models.CASCADE, related_name="testimonials"
    )
    quote = models.TextField(verbose_name="Testimonio")
    author = models.CharField(max_length=120, verbose_name="Autor")
    location = models.CharField(max_length=120, blank=True, verbose_name="Ubicación")
    image = models.ImageField(
        upload_to="eventos/testimonials/",
        help_text="Imagen del autor",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Testimonio de Retiro"
        verbose_name_plural = "Testimonios de Retiro"

    def __str__(self):
        return f"Testimonio de {self.author}"


# ──────────────────────────────────────────────────────────────────────────────
# Página de Terapias
# ──────────────────────────────────────────────────────────────────────────────


class TerapiasPage(models.Model):
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    header = models.OneToOneField(
        "TerapiasHeader",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Header",
    )
    intro = models.OneToOneField(
        "TerapiasIntroSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Introducción",
    )
    benefits_section = models.OneToOneField(
        "TerapiasBenefitsSection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Beneficios",
    )
    second_quote = models.TextField(blank=True, verbose_name="Segunda Cita")
    gallery_section = models.OneToOneField(
        "TerapiasGallerySection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sección de Galería",
    )

    class Meta:
        verbose_name = "6. Página: Terapias"
        verbose_name_plural = "6. Página: Terapias"

    def __str__(self):
        return "Página de Terapias"


class TerapiasHeader(models.Model):
    title = models.CharField(max_length=120, default="Terapias", verbose_name="Título")
    breadcrumb_label = models.CharField(
        max_length=120, default="Terapias", verbose_name="Breadcrumb actual"
    )
    background = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen de fondo del header",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "6.1 Sección: Header de Terapias"
        verbose_name_plural = "6.1 Sección: Header de Terapias"

    def __str__(self):
        return self.title


class TerapiasIntroSection(models.Model):
    main_image = models.ImageField(
        upload_to="eventos/",
        help_text="Imagen principal de la sección de introducción",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=160,
        default="Sanación y Equilibrio para tu Ser",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")
    sidebar_title = models.CharField(
        max_length=160, default="Bienestar", verbose_name="Título del sidebar"
    )
    sidebar_subtitle = models.CharField(
        max_length=160,
        default="Físico, emocional, mental, espiritual",
        verbose_name="Subtítulo del sidebar",
    )
    sidebar_paragraph = models.TextField(blank=True, verbose_name="Párrafo del sidebar")

    class Meta:
        verbose_name = "6.2 Sección: Introducción de Terapias"
        verbose_name_plural = "6.2 Sección: Introducción de Terapias"

    def __str__(self):
        return self.title


class TerapiasBenefitsSection(models.Model):
    title = models.CharField(
        max_length=160, default="Beneficios de Nuestras Terapias", verbose_name="Título"
    )

    class Meta:
        verbose_name = "6.3 Sección: Beneficios de Terapias"
        verbose_name_plural = "6.3 Sección: Beneficios de Terapias"

    def __str__(self):
        return self.title


class TerapiaBenefit(models.Model):
    section = models.ForeignKey(
        TerapiasBenefitsSection, on_delete=models.CASCADE, related_name="benefits"
    )
    title = models.CharField(max_length=120, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "Beneficio de Terapia"
        verbose_name_plural = "Beneficios de Terapias"

    def __str__(self):
        return self.title


class TerapiasGallerySection(models.Model):
    title = models.CharField(
        max_length=160,
        default="Espacios de Contención y Sanación",
        verbose_name="Título",
    )
    paragraph = models.TextField(blank=True, verbose_name="Párrafo")

    class Meta:
        verbose_name = "6.4 Sección: Galería de Terapias"
        verbose_name_plural = "6.4 Sección: Galería de Terapias"

    def __str__(self):
        return self.title


class TerapiasGalleryImage(models.Model):
    section = models.ForeignKey(
        TerapiasGallerySection, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="eventos/gallery/", help_text="Imagen para la galería"
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name="Texto alternativo"
    )

    class Meta:
        verbose_name = "Imagen de la Galería de Terapias"
        verbose_name_plural = "Imágenes de la Galería de Terapias"

    def __str__(self):
        return self.alt_text or f"Imagen {self.id}"
