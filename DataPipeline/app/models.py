from django.db import models

# Create your models here.
class Fund(models.Model):
    regNo = models.CharField(max_length=6, unique=True)
    name = models.TextField()
    fundType = models.IntegerField()
    netAsset = models.BigIntegerField(null=True)

    def __str__(self):
        return self.regNo