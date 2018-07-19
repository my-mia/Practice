
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User 
from django.conf import settings
# Create your models here.
#class Person(models.Model):
    #name = models.CharField(max_length=30)
    #age = models.IntegerField()
 
    #def __str__(self):
    # 在Python3中使用 def __str__(self):
        #return self.name
 
#class IMG(models.Model):
    #img = models.ImageField(upload_to='img')
    #name = models.CharField(max_length=20)
    #def __str__(self):
    # 在Python3中使用 def __str__(self):
        #return self.name

@python_2_unicode_compatible        
class OriImg(models.Model):
    ImgName = models.CharField(u'Original Image Name', max_length=256, null=True)
    img_url = models.ImageField(upload_to='')
    FileDirectoryImg = models.CharField(u'Directory', max_length=256, null=True) 
    CreateTimeImg = models.DateTimeField(u'OriImg Create UTC Time', auto_now_add=True, editable = True, null=True)
    #CreateDat = models.DateTimeField(u'Create Date',auto_now=True, null=True)
    
    def __str__ (self):
        return self.ImgName
    
@python_2_unicode_compatible  
class SegImg(models.Model):
    oriImg = models.ForeignKey(OriImg, on_delete=models.CASCADE)
    SegImgName = models.CharField(u'Segmented Image Name', max_length=100, primary_key=True)
    #SegImgFile= models.ImageField(upload_to='')
    ParentImg = models.CharField(u'Orignial Image Name', max_length=256, null=True)
    FileDirectorySegImg = models.CharField(u'Directory', max_length=256, null=True)
    CreateTimeSeg = models.DateTimeField(u'SegImg Create UTC Time', auto_now_add=True, editable = True, null=True)
    
    def __str__ (self):
        return self.SegImgName



    
#class Meta:
   # db_table='OriImg'
