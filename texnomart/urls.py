from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from texnomart.views import CategoryViewSet, ProductViewSet, ImageViewSet, CommentViewSet, LoginView, LogoutView, \
    LoginJWTView, LogoutJWTView

# Router yaratish
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'images', ImageViewSet)
router.register(r'comments', CommentViewSet)


# Root endpoint uchun maxsus view
class APIRootView(APIView):
    permission_classes = [AllowAny]  # Hamma uchun ochiq

    def get(self, request, *args, **kwargs):
        return Response({
            "categories": request.build_absolute_uri('categories/'),
            "products": request.build_absolute_uri('products/'),
            "images": request.build_absolute_uri('images/'),
            "comments": request.build_absolute_uri('comments/'),
            "login": request.build_absolute_uri('login/'),
            "logout": request.build_absolute_uri('logout/'),
            "login-jwt": request.build_absolute_uri('login-jwt/'),
            "logout-jwt": request.build_absolute_uri('logout-jwt/'),
        })


# URL patterns
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),  # Root endpoint
    path('', include(router.urls)),  # Router URLlari
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login-jwt/', LoginJWTView.as_view(), name='login-jwt'),
    path('logout-jwt/', LogoutJWTView.as_view(), name='logout-jwt'),
]
