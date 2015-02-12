from django.db import models
from django.contrib.auth.models import User


class Whitelisted(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def get_last_login(self):
        users = User.objects.filter(email=self.email).order_by('-last_login')
        if users:
            return users[0].last_login
        else:
            return 'never?'

    def summary(self):
        return '%s active=%s staff=%s super=%s' % (
                self.email, self.is_active, self.is_staff, self.is_superuser)

    def __unicode__(self):
        return self.email
