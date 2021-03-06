from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNUmExpandMethod

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNUmExpandMethod):
    title = models.CharField(max_length=40)
    content = RichTextUploadingField()
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog:%s>" %self.title

    class Meta:
        ordering =['-created_time']

