from django.db import models

class CSVFile(models.Model):
    upload = models.FileField(upload_to='uploads/')
