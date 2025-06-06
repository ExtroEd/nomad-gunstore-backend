import os
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def svg_icon(obj, field_name):
    """
    Returns the contents of the SVG file from the FileField, if it exists.
    """
    file_field = getattr(obj, field_name, None)
    if (file_field and hasattr(file_field, 'path')
            and os.path.exists(file_field.path)):
        try:
            with open(file_field.path, 'r', encoding='utf-8') as f:
                return mark_safe(f.read())
        except Exception as e:
            return f"<!-- SVG error: {e} -->"
    return ''
