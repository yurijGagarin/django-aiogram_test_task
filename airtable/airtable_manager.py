import logging
from collections import defaultdict
from typing import Optional

from airtable.dto import User
from airtable.encrypting import encrypt_password, decrypt_password
from airtable.exceptions import UserAlreadyExist


def get_user(condition) -> Optional[User]:
    users = User.all()
    for user in users:
        if condition(defaultdict(str, user['fields'])):
            return User.from_record(user)
    return None


def create_user(user_id: str, username: str, password: str, tg_username: str, tg_name: str):
    user = get_user(lambda u: u['user_id'] == user_id or u['username'] == username)
    if user is not None:
        raise UserAlreadyExist()
    new_user = User(
        username=str(username),
        password=(encrypt_password(password).decode()),
        user_id=user_id,
        tg_username=tg_username,
        tg_name=tg_name,
    )
    new_user.save()
    logging.info("User saved")
    return new_user


def get_user_by_id(user_id) -> Optional[User]:
    return get_user(lambda u: u['user_id'] == user_id)


def verify_user(username: str, password: str) -> Optional[User]:
    user = get_user(lambda u: u['username'] == username)

    if not user:
        return None

    encrypted_password = decrypt_password(bytes(user.password, 'UTF-8')),
    if password == encrypted_password[0]:
        return user
    return None
