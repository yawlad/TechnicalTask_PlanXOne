from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authapp.views import MyUserViewSet, RegisterUserViewSet
from managerapp.views import TransactionViewSet, StatisticsAPIView
from categoriesapp.views import CategoryViewSet


router = DefaultRouter()
auth_router = DefaultRouter()


router.register(r'users', MyUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'transactions', TransactionViewSet, basename='transactions')


auth_router.register(r'register', RegisterUserViewSet, basename='register')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include(auth_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/statistics/', StatisticsAPIView.as_view()),
    
]
