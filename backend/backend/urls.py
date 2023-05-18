from django.urls import path, include
from rest_framework import routers
from api.views import MovieViewSet, TicketViewSet, CustomerViewSet,UserViewSet,login
from django.contrib import admin

router = routers.DefaultRouter()
router.register('movies', MovieViewSet)
router.register('tickets', TicketViewSet)
router.register('customers', CustomerViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Optional: For login/logout views
    # Add the login URL
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    # Register URLs
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('activate/<str:activation_code>/', UserViewSet.as_view({'get': 'activate'}), name='activate'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('login/', login, name='login'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
