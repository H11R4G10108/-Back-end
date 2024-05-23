from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    username = models.CharField(
        max_length=10,
        help_text="Username")
    email = models.EmailField(
        help_text="The User's email address.", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = None
    last_name = None
    groups = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email


class ShippingInfor(models.Model):
    shipID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         help_text="The user of the shipping information")
    tel = PhoneNumberField(null=False, blank=False, unique=True)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    Is_default = models.BooleanField()


class Status(models.Model):
    class StatusChoice(models.TextChoices):
         Pending = "Pending", "Pending"
         Processing = "Processing", "Processing"
         Shipping = "Shipping", "Shipping"
         Delivered = "Delivered", "Delivered"

    statusID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    status = models.CharField(
        verbose_name="The order's status",
        choices=StatusChoice.choices, max_length=20)


class Size(models.Model):
    class SizeChoice(models.TextChoices):
         S = "S", "S"
         M = "M", "M"
         L = "L", "L"
         XL = "XL", "XL"
         FreeSize = "Free Size", "Free Size"

    sizeID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    status = models.CharField(
        verbose_name="The product's size",
        choices=SizeChoice.choices, max_length=10)


class Category(models.Model):
    catID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, VERBOSE_NAME='ID')
    category = models.CharField(verbose_name="The product's category", max_length=10)


#Product(ProductID, CatID, SizeID, Name, Rating (backend xử lý), Price, Price_afterdiscount (=old-(old*discount)), Stock, Image(đường dẫn dạng related), Description)

class Product(models.Model):
    productID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, VERBOSE_NAME='ID')
    category = models.ForeignKey(
         Category,
         on_delete=models.CASCADE,
         help_text="The category of the product")
    size = models.ForeignKey(
         Size,
         on_delete=models.CASCADE,
         help_text="The size of the product")
    name = models.CharField(verbose_name="The product's name", max_length=50)
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11)
    price_afterdiscount = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11, null=True)
    stock = models.IntegerField(help_text="Stock")
    image = models.ImageField(upload_to="product_image/", verbose_name="The product's image", null=True, default='default.jpg')
    description = models.TextField(help_text="The product description text.")
    def __str__(self):
        return self.name
#Promotion(PromoID, ProductID, Discount(%), Start_date, End_date, Description, Type)


class Promotion(models.Model):
    promoID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, VERBOSE_NAME='ID')
    product = models.ForeignKey(
         Product,
         on_delete=models.CASCADE,
         help_text="The promotion for the product")
