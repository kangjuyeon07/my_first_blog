from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    

class Post(models.Model):
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    
    title = models.CharField(max_length=200)
    
    text = models.TextField()
    
    created_date = models.DateTimeField(
        default=timezone.now
    )
    
    published_date = models.DateTimeField(
        default=None,
        null=True,
        blank=True
    )
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.title
    
        
        
        
        
        