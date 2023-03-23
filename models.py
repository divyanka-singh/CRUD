from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('health', 'Health'),
    ('electronics', 'Electronics'),
    ('travel', 'Travel'),
    ('education', 'Education'),
    ('books', 'Books'),
    ('others', 'Others'),
]

class Expense(models.Model):
    name = models.CharField(max_length=140)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class login(models.Model):
    email = models.CharField(max_length=140)
    password = models.CharField(max_length=140)

    def __str__(self):
        return self.email
