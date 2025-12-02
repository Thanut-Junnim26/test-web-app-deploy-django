from decimal import Decimal
from django.conf import settings
from .models import Medicine

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, medicine, quantity=1, override_quantity=False):
        medicine_id = str(medicine.id)
        if medicine_id not in self.cart:
            self.cart[medicine_id] = {'quantity': 0, 'price': str(medicine.price)}
        if override_quantity:
            self.cart[medicine_id]['quantity'] = quantity
        else:
            self.cart[medicine_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, medicine):
        medicine_id = str(medicine.id)
        if medicine_id in self.cart:
            del self.cart[medicine_id]
            self.save()

    def __iter__(self):
        medicine_ids = self.cart.keys()
        medicines = Medicine.objects.filter(id__in=medicine_ids)
        cart = self.cart.copy()
        for medicine in medicines:
            cart[str(medicine.id)]['medicine'] = medicine
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
