import random
import string


class Helpers:

    @staticmethod
    def generate_random_string(length=8):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_email():
        return f'{Helpers.generate_random_string(10)}@example.com'

    @staticmethod
    def generate_password(length=10):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
