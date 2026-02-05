from django.contrib import admin
from .models import (
    Festival,
    FestivalImage,
    TallerDetail,
    TallerImage,
    TalleresPage,
    TalleresHeader,
    TalleresIntroSection,
    FestivalesPage,
    FestivalesHeader,
    FestivalesIntroSection,
    ArtesPage,
    ArtesHeader,
    ArtesIntroSection,
    ArtesDiversitySection,
    Arte,
    ArtesGallerySection,
    ArtesGalleryImage,
    EscuelaPage,
    EscuelaHeader,
    EscuelaIntroSection,
    EscuelaGalleryImage,
    EscuelaSidebar,
    EscuelaProject,
    RetirosPage,
    RetirosHeader,
    RetirosIntroSection,
    RetirosTypesSection,
    RetiroType,
    RetirosActivitiesSection,
    RetiroActivity,
    RetirosGallerySection,
    RetirosGalleryImage,
    RetirosTestimonialSection,
    RetiroTestimonial,
    TerapiasPage,
    TerapiasHeader,
    TerapiasIntroSection,
    TerapiasBenefitsSection,
    TerapiaBenefit,
    TerapiasGallerySection,
    TerapiasGalleryImage,
)


@admin.register(FestivalesPage)
class FestivalesPageAdmin(admin.ModelAdmin):
    list_display = ("header", "intro")

    def has_add_permission(self, request):
        return not FestivalesPage.objects.exists()


@admin.register(FestivalesHeader)
class FestivalesHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(FestivalesIntroSection)
class FestivalesIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text")


class FestivalImageInline(admin.TabularInline):
    model = FestivalImage
    extra = 1


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "time", "place")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "date",
                    "time",
                    "place",
                    "image",
                    "flyer",
                )
            },
        ),
    )
    inlines = [FestivalImageInline]


class TallerImageInline(admin.TabularInline):
    model = TallerImage
    extra = 1


@admin.register(TalleresPage)
class TalleresPageAdmin(admin.ModelAdmin):
    list_display = ("header", "intro")

    def has_add_permission(self, request):
        return not TalleresPage.objects.exists()


@admin.register(TalleresHeader)
class TalleresHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(TalleresIntroSection)
class TalleresIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text")


@admin.register(TallerDetail)
class TallerDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "schedule", "place", "flyer")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "schedule",
                    "place",
                    "image",
                    "flyer",
                )
            },
        ),
    )
    inlines = [TallerImageInline]


class ArteInline(admin.TabularInline):
    model = Arte
    extra = 1


class ArtesGalleryImageInline(admin.TabularInline):
    model = ArtesGalleryImage
    extra = 1


@admin.register(ArtesPage)
class ArtesPageAdmin(admin.ModelAdmin):
    list_display = ("header", "intro", "diversity", "gallery")

    def has_add_permission(self, request):
        return not ArtesPage.objects.exists()


@admin.register(ArtesHeader)
class ArtesHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(ArtesIntroSection)
class ArtesIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("subtitle", "sidebar_title")


@admin.register(ArtesDiversitySection)
class ArtesDiversitySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [ArteInline]


@admin.register(ArtesGallerySection)
class ArtesGallerySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [ArtesGalleryImageInline]


class EscuelaGalleryImageInline(admin.TabularInline):
    model = EscuelaGalleryImage
    extra = 1


class EscuelaProjectInline(admin.TabularInline):
    model = EscuelaProject
    extra = 1


@admin.register(EscuelaPage)
class EscuelaPageAdmin(admin.ModelAdmin):
    list_display = ("header", "intro", "sidebar")

    def has_add_permission(self, request):
        return not EscuelaPage.objects.exists()


@admin.register(EscuelaHeader)
class EscuelaHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(EscuelaIntroSection)
class EscuelaIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EscuelaGalleryImageInline]


@admin.register(EscuelaSidebar)
class EscuelaSidebarAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EscuelaProjectInline]


class RetiroTypeInline(admin.TabularInline):
    model = RetiroType
    extra = 1


class RetiroActivityInline(admin.TabularInline):
    model = RetiroActivity
    extra = 1


class RetirosGalleryImageInline(admin.TabularInline):
    model = RetirosGalleryImage
    extra = 1


class RetiroTestimonialInline(admin.TabularInline):
    model = RetiroTestimonial
    extra = 1


@admin.register(RetirosPage)
class RetirosPageAdmin(admin.ModelAdmin):
    list_display = (
        "header",
        "intro",
        "types_section",
        "activities_section",
        "gallery_section",
        "testimonial_section",
    )

    def has_add_permission(self, request):
        return not RetirosPage.objects.exists()


@admin.register(RetirosHeader)
class RetirosHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(RetirosIntroSection)
class RetirosIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "sidebar_title")


@admin.register(RetirosTypesSection)
class RetirosTypesSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroTypeInline]


@admin.register(RetirosActivitiesSection)
class RetirosActivitiesSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroActivityInline]


@admin.register(RetirosGallerySection)
class RetirosGallerySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetirosGalleryImageInline]


@admin.register(RetirosTestimonialSection)
class RetirosTestimonialSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [RetiroTestimonialInline]


class TerapiaBenefitInline(admin.TabularInline):
    model = TerapiaBenefit
    extra = 1


class TerapiasGalleryImageInline(admin.TabularInline):
    model = TerapiasGalleryImage
    extra = 1


@admin.register(TerapiasPage)
class TerapiasPageAdmin(admin.ModelAdmin):
    list_display = ("header", "intro", "benefits_section", "gallery_section")

    def has_add_permission(self, request):
        return not TerapiasPage.objects.exists()


@admin.register(TerapiasHeader)
class TerapiasHeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "breadcrumb_label")


@admin.register(TerapiasIntroSection)
class TerapiasIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "sidebar_title")


@admin.register(TerapiasBenefitsSection)
class TerapiasBenefitsSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TerapiaBenefitInline]


@admin.register(TerapiasGallerySection)
class TerapiasGallerySectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TerapiasGalleryImageInline]
