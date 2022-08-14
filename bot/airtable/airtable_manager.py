from typing import List, Dict

from pyairtable.orm import Model, fields

from bot.airtable.encrypting import encrypt_password, decrypt_password
from bot.config import AIRTABLE_API, AIRTABLE_BASE_ID


class Users(Model):
    username = fields.TextField("username")
    password = fields.TextField("password")
    user_id = fields.TextField("user_id")

    class Meta:
        base_id = AIRTABLE_BASE_ID
        table_name = "Users"
        api_key = AIRTABLE_API


new_users = [
    {
        'password': '1234567',
        'user_id': '@max',
        'username': 'max'},
    {
        'password': '134233',
        'user_id': '@kokorin',
        'username': 'kokorin'},
    {
        'password': '123456',
        'user_id': '@yurij',
        'username': 'yurij'},
    {
        'password': '1234567',
        'user_id': '@zimin',
        'username': 'zimin'},
]



def make_user(users: List[Dict]):
    data = users
    for user in data:
        new_user = Users(
            username=str(user['username']),
            password=(encrypt_password(user['password']).decode()),
            user_id=str(user['user_id']),
        )
        new_user.save()
#
# make_user(new_users)
#

def verify_username(username: str, password: str):
    users = Users.all()
    ver_user = {}
    for user in users:
        if user['fields']['username'] == username:
            ver_user = user['fields']
    if not ver_user:
        return "No such user"
    print(ver_user)
    encrypted_password = decrypt_password(bytes(ver_user['password'], 'UTF-8')),
    if password == encrypted_password[0]:
        return True
    return False
# #
#
#
print(verify_username('kokorin', '134233'))
