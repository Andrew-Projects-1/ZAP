from django.db import models
from django.contrib.auth.models import User
import datetime
import time
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image

e = datetime.datetime.now()

# Create your models here.
class QuestionModel(models.Model):
    question_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/%Y/%m/%d/',
        null = True,
    )
    image_description = models.CharField(max_length=280, null=True)

    def __str__(self):
        return self.author.username + ": " + self.question_text + " " + str(self.pub_date.strftime("%b %d, %Y")) + (" %s:%s:%s" % (e.hour, e.minute, e.second)) + " " + str(self.pub_date.strftime("%p"))


class AnswerModel(models.Model):
    answer_text = models.CharField(max_length = 280)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    image = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/answers/%Y/%m/%d/',
        null = True,
    )
    image_description = models.CharField(max_length=280, null=True)




class RantsQuestionModel(models.Model):
    question_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/%Y/%m/%d/',
        null = True,
    )
    image_description = models.CharField(max_length=280, null=True)

    def __str__(self):
        return self.author.username + ": " + self.question_text + " " + str(self.pub_date.strftime("%b %d, %Y")) + (" %s:%s:%s" % (e.hour, e.minute, e.second)) + " " + str(self.pub_date.strftime("%p"))


class RantsAnswerModel(models.Model):
    answer_text = models.CharField(max_length = 280)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(RantsQuestionModel, on_delete=models.CASCADE)
    image = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/answers/%Y/%m/%d/',
        null = True,
    )
    image_description = models.CharField(max_length=280, null=True)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.png', upload_to='profile_pic')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Chat(models.Model):

    #collect in charfield `pk` of all users online 
    users_online = models.CharField(max_length=1500)

class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'



class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    # post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    # comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)