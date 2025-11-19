from rest_framework import viewsets,permissions,filters
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Category, Brand, Product, CartItem, Order, Payment, Like, Contact
from .serializers import *
from rest_framework.authentication import TokenAuthentication
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error':'Username already exists'})
    
    user=User.objects.create_user(username=username,email=email,password=password)
    token=Token.objects.create(user=user)
    return Response({'token':token.key,'user':UserSerializer(user).data})

@api_view(['POST'])
def login_user(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user=authenticate(username=username,password=password)

    if user:
        token, _=Token.objects.get_or_create(user=user)
        return Response({'token':token.key,'user':UserSerializer(user).data})
    else:
        return Response({'error':'Invalid credentials'})
    


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    serializer=UserSerializer(request.user)
    return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all().order_by('-created_at')
    serializer_class=ProductSerializer
    filter_backends=[filters.SearchFilter,filters.OrderingFilter]
    search_fields=['name','description']
    ordering_fields=['price','rating']

class CartItemViewSet(viewsets.ModelViewSet):
    queryset=CartItem.objects.all()
    serializer_class=cartItemSerializer
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContactViewSet(viewsets.ModelViewSet):
    queryset=Contact.objects.all()
    serializer_class=ContactSerializer
    permission_classes=[permissions.AllowAny]