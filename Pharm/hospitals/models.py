#models.py
from django.db import models

from users.models import UserProfile

# Create your models here.

class Insurance(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='insurances')
    insurance_name = models.CharField(verbose_name="InsuranceName", max_length=255)
    # Add other insurance-related fields as needed

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Institution(models.Model):
    """
    Model representing an institution.
    """
    user_profile = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='userprofiles')
    institution_id = models.AutoField(primary_key=True, verbose_name="InstitutionId", unique=True)
    institution_name = models.CharField(verbose_name="InstitutionName", max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City", max_length=100, null=True, blank=True)
    county = models.CharField(verbose_name="County", max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Post Code", max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude", max_length=50, null=True, blank=True)
    reviews = models.ManyToManyField(UserReview, blank=True)
    review_summary=models.CharField(max_length=300,null=False,blank=False)

    def __str__(self):
        return self.institution_name


    # Add a method to get all insuraPharm/hospitals/models.pynces for an institution
    def get_insurances(self):
        return self.insurances.all()

class Service(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='services')
    service_name = models.CharField(max_length=255)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_name} - {self.institution.institution_name}"


 

class UserReview(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return f"{self.review} - {self.institution.institution_name}"




