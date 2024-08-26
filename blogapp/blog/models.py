from django import forms
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    # image = models.CharField(max_length=50)
    image = models.ImageField(upload_to="blogs")
    description = RichTextField()
    is_active = models.BooleanField(default=False)
    is_home= models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True)
    # category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    # category = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    
    # admin sayfasında Blog lar title olarak görünür.#
    def __str__(self):
        return f"{self.title}"
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.blog}'
        pass
    
    pass

