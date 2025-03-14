#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2024
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit this file without direct permission from the author.
# You can redistribute this file without any changes.

class NetSchoolAPIError(Exception):
    pass


class AuthError(NetSchoolAPIError):
    def __init__(self, resp = None):
        self.resp = resp


class SchoolNotFoundError(NetSchoolAPIError):
    def __init__(self, resp = None):
        self.resp = resp


class NoResponseFromServer(NetSchoolAPIError):
    pass