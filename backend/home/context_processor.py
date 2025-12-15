from home.models import Cart

def cart_processor(request):
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)
        return {'cart': cart}
    return {'cart': None}