"""
this .py file contains class for asset data type
"""

import numpy as np
import pandas as pd
from .des_ import encrypt, decrypt


class Asset():
    def __init__(self, asset_name=None, owner=None, value=0):
        self.name = asset_name
        self.owner = owner
        self.value = value  # integer. Value in INR

    def __str__(self):
        k = """[ "name" : {}, "owner" : {}, "value" :{} ]""".format(self.name, self.owner,
                                                                    self.value)
        return k

    def __repr__(self):
        k = """[ name : {}, owner : {}, value :{} ]""".format(self.name, self.owner,
                                                              self.value)
        return k

    def encrypt(self, user):
        dict_ = {
            "name": encrypt(self.name, key=user.password, plaintext_is_hex=False, key_is_hex=False),
            "owner": encrypt(self.owner, key=user.password, plaintext_is_hex=False, key_is_hex=False),
            "value": encrypt(self.value, key=user.password, plaintext_is_hex=False, key_is_hex=False),
        }
        return dict_

    @classmethod
    def decrypt(cls, dict_, user):
        dict_decrypted = {
            "name": decrypt(dict_["name"], key=user.password, return_hex=False, key_is_hex=False),
            "owner": decrypt(dict_["owner"], key=user.password, return_hex=False, key_is_hex=False),
            "value": int(decrypt(dict_['value'], key=user.password, return_hex=False, key_is_hex=False)),
        }
        return Asset(asset_name=dict_decrypted['name'], owner=dict_decrypted['owner'], value=dict_decrypted['value'])

    def to_dict(self):
        dict_ = {
            "name": self.name,
            "owner": self.owner,
            "value": self.value
        }
        return dict_
