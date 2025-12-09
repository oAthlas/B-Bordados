def cart_processor(request):
    return {
        'cart': request.session.get('cart', {})
    }