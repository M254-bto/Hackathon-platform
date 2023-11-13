from django.urls import path, include
from . import views



urlpatterns = [
     path('auth/', include('rest_auth.urls')),
     path('', views.UserViewSet.as_view({'get': 'list'})),
     path('register/', views.UserRegistrationView.as_view(), name='register'),

]
