from rest_framework.serializers import ModelSerializer
from .models import Driver, Car, User, Order


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class DriverSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    user_info = UserSerializer(source='customer')
    driver_info = DriverSerializer(source='driver')
    car_info = CarSerializer(source='car')
    class Meta:
        model = Order
        exclude = ['customer', 'driver', 'car']