from django import template

register = template.Library()

@register.filter
def cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += float(item["price"])
    return total