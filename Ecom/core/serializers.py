from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product, Category, Size, User, CustomerAddress, Order, OrderDetail, Status

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('catID', 'category')

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('sizeID', 'size')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    size = SizeSerializer()

    class Meta:
        model = Product
        fields = ('productID',
                  'category',
                  'size',
                  'name',
                  'price',
                  'price_discounted',
                  'stock',
                  'image',
                  'description')

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'email', 'password')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('addressID', 'user','name','tel','city','street','default')



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # These are claims, you can add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password1": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        validate_password(value)
        return value
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
            model = Order
            fields = ('orderID', 'user','address','customer_name','status','date_order','subtotal','shipping_fee','total_shipping')

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('detailID', 'order', 'product', 'quantity', 'total')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('statusID', 'status')
class OrderReadSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    status = StatusSerializer()
    class Meta:
            model = Order
            fields = ('orderID', 'user','address','customer_name','status','date_order','subtotal','shipping_fee','total_shipping')

class OrderDetailReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderDetail
        fields = ('detailID', 'order', 'product', 'quantity', 'total')