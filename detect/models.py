from django.db import models

# Create your models here.


class UserReg(models.Model):
    name = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    pro_pic = models.FileField(upload_to='pro_pic/',null=True, blank=True,default='pro_pic/user-profile-icon.jpg')
    
    
class PostModel(models.Model):
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE,blank=True)
    post_pic = models.FileField(upload_to='post_pics/',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    likes_count= models.IntegerField(null=True,blank=True)
    liked_users = models.ManyToManyField(UserReg,related_name='liked_posts',default=0)
    created_at= models.DateTimeField(auto_now=True)
    
class CommentSectionModel(models.Model):
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE)
    post=models.ForeignKey(PostModel,on_delete=models.CASCADE)
    comment=models.TextField(null=True,blank=True)
    
class BlockedUsers(models.Model):
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE)
    blocked_status=models.BooleanField(default=False)
    