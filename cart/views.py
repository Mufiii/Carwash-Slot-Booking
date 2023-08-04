from django.shortcuts import get_object_or_404, redirect, render
from home.models import *
from .models import *
from django.http import HttpResponse
# Create your views here.

def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart

def add_cart(request,product_id):
    product = CarWashPackage.objects.get(id= product_id) # get the product
    try :
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart_id present in the session
    except Cart.DoesNotExist :
        cart = Cart.objects.create(
          cart_id = _cart_id(request)
        )
    cart.save()
    
    try :
         # Try to get the cart item with the given product and cart
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # If the product is already in the cart, update the quantity
        cart_item.quantity += 1
        # Save the cart item to the database
        cart_item.save()
    except CartItem.DoesNotExist:
      cart_item = CartItem.objects.create(
          product = product,
          quantity = 1,
          cart = cart,
      )
      cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')
  
  

def cart(request,totel=0,quantity=0,cart_items=None):
  try :
      # Try to get the cart associated with the user's session using _cart_id(request)
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart,is_active=True)
      for cart_item in cart_items:
        totel += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
  except Cart.DoesNotExist:
    pass # just ignore
  context = {
    'totel':totel,
    'quantity':quantity,
    'cart_items':cart_items
  }
  return render(request, 'cart/cart.html',context)

def remove_cart(request,product_id):
  cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cart
  product = get_object_or_404(CarWashPackage,id = product_id) # it returns either product or 404
  cart_item = CartItem.objects.get(product=product,cart=cart)
  cart_item.delete()
  return redirect('cart')

