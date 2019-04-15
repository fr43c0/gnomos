from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Permitidos(models.Model):
  email=models.EmailField(unique=True, max_length=254)
  
  def get_absolute_url(self):
      return reverse("detalhe", kwargs={"pk": self.pk})
  
  def __str__(self):
      return self.email
  class Meta:
      verbose_name_plural = 'Permitidos'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

