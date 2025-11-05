from django.db import models
from django.core.validators import EmailValidator, MaxLengthValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[
        MaxLengthValidator(50, "Category name cannot exceed 50 characters")
    ])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=200, validators=[
        MaxLengthValidator(100, "Title cannot be longer than 100 characters")
    ])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author_email = models.EmailField(validators=[EmailValidator(message="Enter a valid email address")])
    is_featured = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title