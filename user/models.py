from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from PIL  import Image
from django.shortcuts import render
from django.db.models import Q
import datetime 
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render,redirect

post_category=(
    ('R','Request'),
    ('D','Donation'),
)
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug_title = models.CharField(max_length=100,null=True)
    content = models.TextField()
    image = models.ImageField(default='a.jpg',upload_to='medicament_images')
    expirattion_date = models.DateField(auto_now=True)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    current_place =models.CharField(max_length=50)
    show_post =models.CharField(max_length=6)
    isDonated = models.CharField(max_length=6,default="no")
    isReceived = models.CharField(max_length=6,default="no")
    post_type = models.CharField(choices=post_category,null=True,max_length=100)

    def __str__(self):
        return 'Type: {} - {} , created by {} on {}'.format(self.post_type,self.title,self.author,self.post_date.date())
    @staticmethod
    def create_request(request) :
        title = request.POST['object']
        slug_title = str(title).replace(" ","-").strip('-')
        content = request.POST['content']
        c_place = request.POST['c_place']
        author = request.user
        newpost = Post(
                    post_type ='R',
                    title=title,
                    slug_title =slug_title,
                    current_place=c_place,
                    content=content,
                    author=author,
                    show_post="yes",
                    )
        newpost.save()
        return newpost
       

    @staticmethod
    def create_donation(request):
        title = request.POST['object']
        slug_title = str(title).replace(" ","-").strip('-')
        content = request.POST['content']
        c_place = request.POST['c_place']
        expirattion_date = request.POST['expirattion_date']
        author = request.user
        newpost = Post(
            post_type= 'D',
            title = title,
            slug_title =slug_title,
            current_place=c_place,
            content=content,
            author=author,
            expirattion_date = expirattion_date,
            show_post="yes",
            )
        try:
            img = request.FILES['image']
            newpost.image = img
        except:
            pass
        newpost.save()
        return newpost
        
    @staticmethod
    def update_post():
        pass
    @staticmethod
    def delete_post():
        pass



    class Meta:
        ordering = ('expirattion_date', )


class Notification(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receiver',on_delete=models.CASCADE) 
    sender = models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE ,null=True) 
    notification_date =models.DateTimeField(default=timezone.now)
    status =models.CharField(max_length=6)
    type =  models.CharField(choices=post_category,null=True,max_length=100)
    def __str__(self):
        return f'{self.type} : from {self.sender} to {self.post.author} about {self.post.post_type}'
    @staticmethod
    def create_notification():
        pass

    class Meta:
        ordering =('-notification_date',)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    phone_number = models.CharField(max_length=12)

    #email_verif = random code created while registeration
    #others ...


    def __str__(self):
        return f'{self.user} profile '
        #resize photo 
    """def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)"""

def create_profile(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
    

post_save.connect(create_profile,sender=User)
