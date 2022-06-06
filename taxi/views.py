from django.db.utils import IntegrityError
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import AuthenticationFailed, ParseError, ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
import django_filters.rest_framework
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Driver, Car, Order, User
from .serializers import DriverSerializer, CarSerializer, OrderSerializer, UserSerializer


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.filter(Q(status='ACTIVE') | Q(status='DONE'))
    serializer_class = OrderSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['status', 'driver', 'car']


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register', url_name='register')
    def register(self, request):
        if 'email' not in request.data:
            raise ParseError({'message': 'Email cannot be empty'})

        if 'password' not in request.data:
            raise ParseError({'message': 'Password cannot be empty'})

        try:
            user = User.objects.create_user(email=request.data['email'], first_name=request.data['first_name'])
            user.set_password(request.data['password'])
            user.is_active = True
            user.save()
            return Response({'message': 'success'})
        except IntegrityError:
            return Response({'message': 'User with this email already exist'})


    @action(methods=['POST'], detail=False)
    def login(self, request):
        if 'email' not in request.data:
            raise ValidationError({'email': ['Email must be provided']})
        if 'password' not in request.data:
            raise ValidationError({'password': ['Password must be provided']})

        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound({'message': 'User with provided credentials does not exist'})

        if not user.check_password(request.data.get('password')):
            raise AuthenticationFailed({'message': 'Incorrect password'})

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token)}
        return response

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated], url_path='me')
    def user(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data)

    @action(detail=True, methods=['POST'], url_path='change_password')
    def change_password(self, request, pk=None):
        if 'new_password' not in request.data:
            raise ValidationError({'new_password': 'Password must be provided'})
        password = request.data['new_password']
        user = User.objects.get(id=pk)
        user.set_password(password)
        user.save()
        return Response({'status': 'password changed'})
