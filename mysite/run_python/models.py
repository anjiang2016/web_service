# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
#from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import datetime
class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    def __unicode__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1) 
class Choice(models.Model):
    question=models.ForeignKey(Question)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text

class Blog(models.Model):
    title = models.CharField(max_length=50,verbose_name="标题")
    content = RichTextField(blank=True,null=True,verbose_name="内容")
def __unicode__(self):
    return self.name
class Post(models.Model):
    content = RichTextUploadingField(null=True, blank=True)
