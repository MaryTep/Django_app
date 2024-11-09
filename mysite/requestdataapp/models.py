from django.db import models
from requestdataapp.for_validate.for_validate import validate_file_size, validate_ip


class MyFile(models.Model):
    name = models.CharField(max_length=100)
    size = models.BigIntegerField(validators=[validate_file_size])


class UserIp(models.Model):
    class Meta:
        ordering = ["user_ip"]

    user_ip = models.CharField(null=False, blank=False, max_length=20, validators=[validate_ip])
    time_run = models.CharField(null=False, blank=False, max_length=30)


class Files(models.Model):
    image = models.FileField()

    def __str__(self):
        return str(self.field_names)

