from django.db import models

# Create your models here.
class Review(models.Model):
    user = models.CharField(default='Anonymous', max_length=100)
    description = models.CharField(max_length=4000)
    stars = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.user} rated {self.stars} stars and said {self.description}"

class Equipment(models.Model):
    image = models.ImageField(upload_to='equipment', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}: {self.description}"