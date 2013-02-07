from django.db import models


class Whitelisted(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

# eof
