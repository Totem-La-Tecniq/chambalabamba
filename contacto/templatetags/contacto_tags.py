from django import template

register = template.Library()


@register.filter(name="add_error_class")
def add_error_class(field):
    attrs = field.field.widget.attrs.copy()
    if field.errors:
        attrs["class"] = attrs.get("class", "") + " error"
    return field.as_widget(attrs=attrs)


# Custom template tags para contacto
