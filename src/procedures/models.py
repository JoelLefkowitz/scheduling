from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class Patient(models.Model):
    patient_id = EncryptedCharField(max_length=200, unique=True)
    first_name = EncryptedCharField(max_length=200)
    last_name = EncryptedCharField(max_length=200)


class Procedure(models.Model):
    schedule_id = models.CharField(max_length=75)
    procedure_code = models.CharField(max_length=50)
    procedure_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
