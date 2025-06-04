from django.db import models

# Create your models here.

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)  # Add unique=True or primary_key=True if needed
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.emp_name
