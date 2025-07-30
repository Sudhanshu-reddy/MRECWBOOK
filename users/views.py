from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
from users.models import UserRegistrationModel,BookModel,CartModel,OrderModel
from django.db.models import Q

def UserHome(request):
    userid = request.session['userid']
    username = request.session['username']
    messages.success(request, f"Welcome {username}!")
    data = BookModel.objects.all() 
    return render(request, 'users/UserHome.html', {'data':data})


def SearchBooks(request):
    query = request.GET.get('query', '')  # get 'query' parameter from form
    data = []

    if query:
        data = BookModel.objects.filter(
            Q(bookname__icontains=query) |
            Q(bookauthor__icontains=query) |
            Q(bookid__icontains=query)
        )
        if not data:
            messages.info(request, "No books found for your search.")

    return render(request, 'users/SearchBooks.html', {'data': data, 'query': query})

def viewBooks():
    return "Hello Im viewBooks"

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BookModel, CartModel

def AddToCart(request):
    if request.method == "GET":
        book_id = request.GET.get('bookid')

        username = request.session.get('username')
        if not username:
            messages.error(request, "Please login first.")
            return redirect('UserLogin')

        try:
            book = BookModel.objects.get(bookid=book_id)
        except BookModel.DoesNotExist:
            messages.error(request, "Book not found.")
            return redirect('SearchBooks')

        existing = CartModel.objects.filter(username=username, bookid=book_id).first()
        if existing:
            existing.quantity += 1
            existing.save()
            messages.success(request, "Book quantity updated in cart.")
        else:
            CartModel.objects.create(
                username=username,
                bookid=book.bookid,
                bookname=book.bookname,
                price=book.price,
                quantity=1
            )
            messages.success(request, "Book added to cart.")

        return redirect('SearchBooks')  

    return redirect('SearchBooks')
 
 
def ViewCart(request):
    data = CartModel.objects.all()
    for item in data:
        item.total = float(item.price) * item.quantity
    return render(request, 'users/ViewCart.html', {'data': data})


def DeleteCartItem(request, id):
    CartModel.objects.filter(id=id).delete()
    return redirect('ViewCart')




def IncreaseQty(request, id):
    cart_item = CartModel.objects.get(id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('ViewCart')

def DecreaseQty(request, id):
    cart_item = CartModel.objects.get(id=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('ViewCart')


def CheckOut():
    return "Hello Im CheckOut"



def CheckOut(request):
    username = request.session.get('username')
    cart_items = CartModel.objects.filter(username=username)

    return render(request, 'users/checkout.html', {'cart_items': cart_items})


def CheckOutAction(request):
    if request.method == "POST":
        username = request.session.get('username')
        delivery_address = request.POST.get('delivery_address')
        payment_mode = request.POST.get('payment_mode')
        

        cart_items = CartModel.objects.filter(username=username)
        if not cart_items:
            messages.error(request, "Cart is empty.")
            return redirect('CheckOut')

        # Combine all items into a single order
        booknames = ', '.join([item.bookname for item in cart_items])
        bookids = ', '.join([item.bookid for item in cart_items])
        quantities = ', '.join([str(item.quantity) for item in cart_items])
        total_price = sum(float(item.price) * item.quantity for item in cart_items) 
        card_details = request.POST.get('card_details') if payment_mode == "Card" else "Nill"
        payment_status = ""
        if payment_mode == "Card":
            payment_status = "Paid"
        else:
            payment_status = "Pending"


        OrderModel.objects.create(
            username=username,
            booknames=booknames,
            bookids=bookids,
            total_price=str(total_price),
            quantities=quantities,
            delivery_address=delivery_address,
            payment_mode=payment_mode,
            card_details=card_details if payment_mode == "Card" else "Cash on Delivery",
            payment_status=payment_status,
        )

        cart_items.delete()

        messages.success(request, "Order placed successfully.")
        return redirect('UserHome')  

    return redirect('CheckOut')



def Payment():
    return "Hello Im Payment"

def OrderDetails(request):
    data= OrderModel.objects.all()
    return render(request, 'users/OrderDetails.html', {'data': data})
 

def UserLogout(request):
    del request.session['userid']
    del request.session['username']
    return redirect('index')
