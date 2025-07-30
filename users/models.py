from django.db import models

class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistration'


# Create your models here.
class BookModel(models.Model):
    bookname = models.CharField(max_length=100)
    bookid = models.CharField(unique=True, max_length=100)
    bookauthor = models.CharField(max_length=100)
    publishyear = models.CharField( max_length=100)
    price  = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    stock  = models.CharField(max_length=100)
    cover_image  = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'Book'

class CartModel(models.Model):
    username = models.CharField(max_length=100)
    bookid = models.CharField(max_length=100)
    bookname = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.username} - {self.bookname}"

    class Meta:
        db_table = 'Cart'


class OrderModel(models.Model):
    username = models.CharField(max_length=100)
    booknames = models.CharField(max_length=255)
    bookids = models.CharField(max_length=255)
    total_price = models.CharField(max_length=100)
    quantities = models.CharField(max_length=100)
    
    delivery_address = models.TextField()
    payment_mode = models.CharField(max_length=100)
    card_details = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=100, default="Pending")
    
    order_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Orders"

