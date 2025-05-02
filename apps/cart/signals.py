from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart


@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    for item in guest_cart.items.all():
        existing_item = user_cart.items.filter(product=item.product).first()
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
        else:
            item.cart = user_cart
            item.pk = None
            item.save()

    guest_cart.delete()
