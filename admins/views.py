from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import UserRegistrationModel,BookModel
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
import random
import string
# Create your views here.

def AdminHome(request):
    return render(request, 'admins/AdminHome.html')

def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/ViewRegisterUsers.html', {'data':data})

def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'Approved'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/ViewRegisterUsers.html', {'data': data})

def AdminDeleteUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        UserRegistrationModel.objects.filter(id=id).delete()
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/ViewRegisterUsers.html', {'data': data})

def AddBookAction(request):
    if request.method == "POST":
        bookname = request.POST.get('bookname')
        bookid = request.POST.get('bookid')
        bookauthor = request.POST.get('bookauthor')
        publishyear = request.POST.get('publishyear')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        image_file = request.FILES.get('Imagepath')
        status = request.POST.get('status')

        ext = os.path.splitext(image_file.name)[1] 
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        random_filename = f"{random_str}{ext}"
        fs = FileSystemStorage(location='media/')        
        filename = fs.save(random_filename, image_file)
        imagepath = os.path.join('media/',    )

        BookModel.objects.create(
            bookname=bookname,
            bookid=bookid,
            bookauthor=bookauthor,
            publishyear=publishyear,
            price=price,
            description=description,
            stock=stock,
            cover_image=imagepath,
            status=status
        )

        messages.success(request, "Book added successfully!")
        return render(request, 'admins/AddBook.html')


def AddBooks(request):
        return render(request, 'admins/AddBook.html')

def ViewBooks(request):
    data = BookModel.objects.all()
    return render(request, 'admins/ViewBooks.html', {'data':data})

def deleteBooks():
    return "Hello Im ModifyBooks"

def ViewOrders():
    return "Hello Im ViewOrders"
