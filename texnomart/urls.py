# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView, LogoutView, LoginJWTView, LogoutJWTView

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Token Authentication
    path('login/token/', LoginView.as_view(), name='login_token'),
    path('logout/token/', LogoutView.as_view(), name='logout_token'),

    # JWT Authentication
    path('login/jwt/', LoginJWTView.as_view(), name='login_jwt'),
    path('logout/jwt/', LogoutJWTView.as_view(), name='logout_jwt'),
]
