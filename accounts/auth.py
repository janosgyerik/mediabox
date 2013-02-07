from django.contrib.auth.models import User

from django_openid_auth.auth import OpenIDBackend

from accounts.models import Whitelisted


class WhitelistedOpenIDBackend(OpenIDBackend):

    def create_user_from_openid(self, openid_response):
        details = self._extract_user_details(openid_response)

        email = details['email'] or ''

        whitelisted = self.get_whitelisted(email)
        if whitelisted:
            nickname = details['nickname'] or 'openiduser'
            username = self._get_available_username(
                    details['nickname'], openid_response.identity_url)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username, email, password=None)
            self.associate_openid(user, openid_response)
            self.update_user_details(user, details, openid_response)
            user.is_active = whitelisted.is_active
            user.is_staff = whitelisted.is_staff
            user.is_superuser = whitelisted.is_superuser
            user.save()
        else:
            user = None

        return user

    def get_whitelisted(self, email):
        try:
            return Whitelisted.objects.get(email=email)
        except Whitelisted.DoesNotExist:
            return None

# eof
