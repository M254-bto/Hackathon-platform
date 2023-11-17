from django.urls import path, include
from . import views

urlpatterns = [
     path('auth/', include('rest_auth.urls')),
     path('', views.UserViewSet.as_view({'get': 'list'})),
     path('register/', views.UserRegistrationView.as_view(), name='register'),
     path('teams/', views.team_list_create_view, name='team-list-create'),
     path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
     path('teams/join/<int:team_id>/', views.JoinTeamView.as_view(), name='join-team'),
     path('upload/', views.FileUploadView.as_view(), name='file-upload'),
     path('leaderboard/', views.get_accuracy_scores, name='leaderboard'),


]
