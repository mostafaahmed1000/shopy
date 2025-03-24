from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    if field.field.widget.attrs.get('class'):
        field.field.widget.attrs['class'] += ' ' + css_class
    else:
        field.field.widget.attrs['class'] = css_class
    return field
