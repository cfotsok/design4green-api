from django.db import models


class Website(models.Model):
    url = models.CharField(max_length=300)
    score = models.FloatField(max_length=5, default=0.0)

    def __str__(self):
        return self.url


class Criteria(models.Model):
    class StateChoices(models.TextChoices):
        COMPLIANT = "conforme"
        UNDER_DEPLOYMENT = "en cours de déploiement"
        IMPROPER = "non conforme"
        NON_APPLICABLE = "non applicable"

    number = models.CharField(max_length=6)
    state = models.CharField(
        choices=StateChoices.choices,
        max_length=23
    )
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.state}"
