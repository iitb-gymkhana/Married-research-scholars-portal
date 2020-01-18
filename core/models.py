from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """ Defines a one to one mapping to User field to store additonal info such as the starting user is associated with, or any other domains user might have. """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=7)
    hostel = models.CharField(max_length=7)
    hostel_name = models.CharField(max_length=10)  # Not required though

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
