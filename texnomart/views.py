from django.contrib import admin
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Category, Product, Image, Comment
from .permissions import WeekdayOnlyPermission
from .serializers import CategorySerializer, ProductSerializer, ImageSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers  # Yangi qo'shildi


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        return obj.user == request.user if request.user.is_authenticated else False


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('products').order_by('name')
    serializer_class = CategorySerializer
    filter_backends = []

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('images', 'likes').order_by('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price']
    permission_classes = [WeekdayOnlyPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.select_related('product').order_by('product__name')
    serializer_class = ImageSerializer
    filter_backends = []

    # Agar /images/ ni ham autentifikatsiyasiz ochmoqchi bo'lsangiz:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related('product', 'user').order_by('created_at')
    permission_classes = [WeekdayOnlyPermission, IsCommentOwner]

    def get_queryset(self):
        if timezone.now().weekday() > 4:  # Hafta oxiri bo‘lsa bo‘sh queryset
            return Comment.objects.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        if not product_id:
            raise serializers.ValidationError({"product_id": "Ushbu maydon majburiy."})  # Tuzatildi
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None, product=product)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        time_elapsed = timezone.now() - instance.created_at
        if time_elapsed > timedelta(minutes=1):
            raise PermissionDenied("Sharhni o‘chirish uchun 1 daqiqadan ko‘p vaqt o‘tdi.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        time_elapsed = timezone.now() - instance.created_at
        if time_elapsed > timedelta(minutes=2):
            raise PermissionDenied("Sharhni yangilash uchun 2 daqiqadan ko‘p vaqt o‘tdi.")
        return super().update(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"detail": "Noto‘g‘ri login yoki parol"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({"detail": "Muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)
        return Response({"detail": "Foydalanuvchi autentifikatsiya qilinmagan."}, status=status.HTTP_400_BAD_REQUEST)


class LoginJWTView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Noto‘g‘ri login yoki parol"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutJWTView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
