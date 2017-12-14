from django.db import models

# Create your models here.



from django.db import models

class Role(models.Model):
    name= models.CharField(max_length=32,verbose_name='角色名')
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    username= models.CharField(max_length=32)

    def __str__(self):
        return self.username

class UserType(models.Model):
    caption= models.CharField(max_length=32)

    def __str__(self):
        return self.caption

class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='文章标题')
    def __str__(self):
        return self.title
