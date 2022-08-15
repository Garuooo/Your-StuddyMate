from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# we will create our db here


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    username = models.CharField(unique=True,max_length=200)
    avatar = models.ImageField(null=True, default="avatar.svg")
    REQUIRED_FIELDS = []
    
 

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User, related_name="participants",blank="true") # we use related name cause we have already a relation which involves User
    #null is true
    #blank = true // can be empty when we use save()
    # participants = 
    update = models.DateTimeField(auto_now=True)
    # auto_now runs  every time save method is called 
    created = models.DateTimeField(auto_now_add = True)
    # auto_now runs the first time save method is called 
    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["-created","-update"]

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    room_topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    def __str__ (self):
        return self.body[0:50]
    class Meta:
        ordering = ["-created","-updated"]
