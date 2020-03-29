from django.db import models

# Create your models here.
class Contact(models.Model):
    group_id = models.IntegerField(null=True, blank=True)
    patient_id = models.IntegerField(null=True, blank=True)
    patient_account_num = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    middle_initial = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    dob = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=50, blank=True)
    cur_street1 = models.CharField(max_length=50, blank=True)
    cur_street2 = models.CharField(max_length=50, blank=True)
    cur_city = models.CharField(max_length=50, blank=True)
    cur_zip = models.IntegerField(null=True, blank=True)
    prev_first_name = models.CharField(max_length=50, blank=True)
    prev_middle_initial = models.CharField(max_length=50, blank=True)
    prev_last_name = models.CharField(max_length=50, blank=True)
    prev_street_1 = models.CharField(max_length=50, blank=True)
    prev_street_2 = models.CharField(max_length=50, blank=True)
    prev_city = models.CharField(max_length=50, blank=True)
    prev_state = models.CharField(max_length=50, blank=True)
    prev_zip = models.IntegerField(null=True, blank=True)

