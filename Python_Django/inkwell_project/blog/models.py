from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Similar to defining a Mongoose schema
    title = models.CharField(max_length=200)  # Like String field
    content = models.TextField()  # Like longer text field
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Like reference
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title  # For admin display

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"