from .models import Cart
# from django.template import RequestContext

def cart_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer = customer, complete=False)
        items = order.cartitem_set.all()
        cartitem = order.get_cart_items
    else:
        items = []    
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitem = order['get_cart_items']    
    return {'items':items, 'order':order, 'cartitem' : cartitem}