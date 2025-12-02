from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Category, Medicine, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    medicines = Medicine.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        medicines = medicines.filter(category=category)
    return render(request, 'store/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'medicines': medicines})

def product_detail(request, id, slug):
    medicine = get_object_or_404(Medicine,
                                 id=id,
                                 slug=slug,
                                 available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product/detail.html',
                  {'medicine': medicine,
                   'cart_product_form': cart_product_form})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Medicine, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(medicine=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('store:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Medicine, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'store/cart/detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         medicine=item['medicine'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'store/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'store/order/create.html',
                  {'cart': cart, 'form': form})
