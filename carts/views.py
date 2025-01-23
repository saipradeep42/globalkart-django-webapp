from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# def add_cart(request, product_id):
#     product = Product.objects.get(id=product_id) # this will get the product with id
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]  # added later for variation
            
#             try:
#                 variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_iexact=value)
#                 product_variation.append(variation)
#                 # print(variation)                
#             except:
#                 pass
    
#     try:
#         cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id using the session
#     except Cart.DoesNotExist: # this exception is to handle if cart does not exist
#         cart = Cart.objects.create(cart_id = _cart_id(request))
#     cart.save() 
    
#     # Here we combine the product and cart to become a cart item - 1 cart can have multiple products
#     try:
#         cart_item  = CartItem.objects.create(product = product, quantity = 1, cart = cart)
#         if len(product_variation) > 0:
#             cart_item.variations.clear()
#             for item in product_variation:
#                 cart_item.variations.add(item)
#         # cart_item.quantity += 1 # increment quantity by 1 for  each product which is added to cart (directly passing as argument so not needed)
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             product = product,
#             quantity = 1,
#             cart = cart,
#         ) #here quantity=1 means when you add the product to cart it will add only 1 item to the cart at a time
#         if len(product_variation) > 0:
#             cart_item.variations.clear()
#             for item in product_variation:
#                 cart_item.variations.add(item)
#         cart_item.save()
#     return redirect('cart')


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product by ID
    product_variation = []

    # Extract product variations from POST data
    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                # Get the variation based on category and value
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Retrieve or create a cart using the session cart_id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Check if the cart item with the same product and variations already exists
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        # Check if the existing cart item matches the current variations
        existing_variations = [list(item.variations.all()) for item in cart_items] #using list comprehension here
        ids = [item.id for item in cart_items]

        if product_variation in existing_variations:
            # Increment quantity if variations match
            index = existing_variations.index(product_variation)
            cart_item = CartItem.objects.get(id=ids[index])
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Create a new cart item if variations do not match
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if product_variation:
                cart_item.variations.set(product_variation)
            cart_item.save()
    else:
        # Create a new cart item if none exists for the product
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if product_variation:
            cart_item.variations.set(product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass    
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()    
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        # Set defaults if the cart object does not exist
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'store/cart.html', context)



