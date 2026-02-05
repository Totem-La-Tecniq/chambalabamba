from django.contrib import admin
from .models import ContactoStatic

# @admin.register(Contacto)
# class ContactoAdmin(admin.ModelAdmin):
#    list_display = ('name', 'email', 'subject', 'created_at')
#    list_filter = ('created_at',)
#    search_fields = ('name', 'email', 'subject', 'message')
#    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

#    def has_add_permission(self, request):
#        return False

#    def has_delete_permission(self, request, obj=None):
#        return True


@admin.register(ContactoStatic)
class ContactoStaticAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Header", {"fields": ("titulo_superior", "titulo")}),
        ("Blockquote", {"fields": ("blockquote_text", "blockquote_footer")}),
        ("Información de Contacto", {"fields": ("direccion", "telefono", "email")}),
        ("Mapa", {"fields": ("google_maps_iframe",)}),
    )

    def has_add_permission(self, request):
        return self.model.objects.count() == 0
