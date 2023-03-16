from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    password = models.CharField(max_length=200)
    title = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def clean(self):
        if not self.title and self.website:
            self.title = self.website
        if not self.title and not self.website:
            raise ValidationError
        return self
