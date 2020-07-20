from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Role(models.Model):

	STUDENT = 1
	DJELATNIK = 2

	ROLE_CHOICES = (
	    (STUDENT, 'student'),
	    (DJELATNIK, 'djelatnik'),
	)

	id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

	def __str__(self):
	    return self.get_id_display()

class User(AbstractUser):
  roles = models.ManyToManyField(Role)