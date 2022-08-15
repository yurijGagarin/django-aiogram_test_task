from django.contrib.auth.backends import BaseBackend

from airtable.airtable_manager import verify_user, get_user_by_id


class AuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        user = verify_user(str(username), str(password))
        if user is not None:
            return user.get_django_user()

        return None

    def get_user(self, user_id):
        user = get_user_by_id(user_id)
        if user is None:
            return None
        return user.get_django_user()
