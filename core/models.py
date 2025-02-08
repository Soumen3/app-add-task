from django.db import models
from django.contrib.auth.models import User

class App(models.Model):
    name = models.CharField(max_length=100)
    app_link = models.URLField(max_length=300,default="/")  # App link field
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, null= True, blank=True)  # New sub-category field
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to="screenshots/")

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"
