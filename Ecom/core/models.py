from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(max_length=10, help_text="Username", unique=True)
    email = models.EmailField(help_text="The User's email address.", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = None
    last_name = None
    groups = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class CustomerAddress(models.Model):
    addressID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user of the shipping information.")
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=10,
                           validators=[
                               RegexValidator(
                                   regex=r'(03|05|07|08|09|01[2|6|8|9])+([0-9]{8})\b',
                                   message="Enter a valid phone number.",
                                   code="invalid_phonenumber",
                               ),
                           ], )
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    default = models.BooleanField()

    def __str__(self):
        return self.name


class Status(models.Model):
    class StatusChoice(models.TextChoices):
        Pending = "Pending", "Pending"
        Processing = "Processing", "Processing"
        Shipping = "Shipping", "Shipping"
        Delivered = "Delivered", "Delivered"
        Canceled = "Canceled", "Canceled"

    statusID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    status = models.CharField(
        verbose_name="The order's status",
        choices=StatusChoice.choices, max_length=20, default='Pending')

    def __str__(self):
        return self.status


class Size(models.Model):
    class SizeChoice(models.TextChoices):
        S = "S", "S"
        M = "M", "M"
        L = "L", "L"
        XL = "XL", "XL"
        FreeSize = "Free Size", "Free Size"

    sizeID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    size = models.CharField(
        verbose_name="The product's size",
        choices=SizeChoice.choices, max_length=10)

    def __str__(self):
        return self.size


class Category(models.Model):
    catID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    category = models.CharField(verbose_name="The product's category", max_length=50)

    def __str__(self):
        return self.category


class Product(models.Model):
    productID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="The category of the product")
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        help_text="The size of the product")
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, default=0, max_digits=65)
    price_discounted = models.DecimalField(decimal_places=2, default=0, max_digits=65, blank=True, null=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="product_image/", verbose_name="The product's image",
                              null=True, default='default.jpg')
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    promoID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The promotion for the product")
    discount = models.DecimalField(decimal_places=2, max_digits=65)
    type = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.product


class ProductReview(models.Model):
    reviewID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user of the shipping information")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The promotion for the product")
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(null=True)
    date_review = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product


class Order(models.Model):
    orderID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user of the order",
        related_name="user_fk")
    address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.CASCADE,
        help_text="The shipping ìnformation of the order",
        related_name="address_fk"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        help_text="The status of the order",
        related_name="status_fk")
    customer_name = models.TextField(max_length=256)
    date_order = models.DateTimeField(default=timezone.now)
    # date_order = models.DateField(default=timezone.now)
    # time_order = models.TimeField(auto_now_add=True)
    subtotal = models.DecimalField(decimal_places=2, max_digits=65)
    shipping_fee = models.DecimalField(decimal_places=2, max_digits=65, default=5)
    total_shipping = models.DecimalField(decimal_places=2, max_digits=65)
    def __str__(self):
        return self.customer_name


class OrderDetail(models.Model):
    detailID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        help_text="The order that the detail belongs to")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The product in the detail")
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(decimal_places=2, max_digits=65)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    # def get_total_item_price(self):
    #     return self.quantity * self.product.price
    #
    # def get_total_discount_item_price(self):
    #     return self.quantity * self.product.price_discounted
    #
    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()
    #
    # def get_final_price(self):
    #     if self.product.price_discounted:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()
