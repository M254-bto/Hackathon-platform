from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TeamSerializer, MemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from .models import Team, Member







class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_destroy(self, serializer):
        serializer.save(user=self.request.user)



class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Override the create method to hash the password before saving the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Manually set the password, as the serializer only returns hashed passwords
        user.set_password(request.data['password'])
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



# class TeamCreateView(generics.CreateAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#     def perform_create(self, serializer):
#         # Set the created_by field based on the authenticated user
#         serializer.save(created_by=self.request.user)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def team_list_create_view(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        
        data = request.data
        data['created_by'] = request.user.id
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer



#add member to team
class JoinTeamView(generics.CreateAPIView):
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        team_id = self.kwargs.get('team_id')
        
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already a member of a team
        if Member.objects.filter(user=user).exists():
            return Response({'error': 'User is already a member of a team'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new member
        serializer = self.get_serializer(data={'user': user.id, 'team': team_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)