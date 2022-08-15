from pyairtable.orm import Model, fields

from bot.config import AIRTABLE_API, AIRTABLE_BASE_ID


class User(Model):
    username = fields.TextField("username")
    tg_username = fields.TextField("tg_username")
    tg_name = fields.TextField("tg_name")
    password = fields.TextField("password")
    user_id = fields.IntegerField("user_id")

    class Meta:
        base_id = AIRTABLE_BASE_ID
        table_name = "Users"
        api_key = AIRTABLE_API

    def get_django_user(self):
        from airtable.models import DjangoUser
        return DjangoUser(username=self.username, id=self.user_id, tg_username=self.tg_username, tg_name=self.tg_name)
