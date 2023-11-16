from django.db import models
from django.contrib.auth.models import User




class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team_created_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username