from django.db import models

class Tos(models.Model):
	version = models.CharField(max_length=50)

	date = models.DateField()

	terms = models.TextField()