"""
Transaction class
"""
import base64
import datetime
from .rsa_ import rsa_encrypt,rsa_decrypt
import rsa

from .des_ import encrypt, decrypt
from hashlib import sha256
import json
from .utils import tuple_


class Transaction():
    def __init__(self, time=None, user_object=None, user_name=None, amount=0, asset=None,
                 type_of_txn=None, digital_signature = None, privk = None, pubk = None):
        self.time = time
        self.user_object = user_object
        # print("self.user_object", self.user_object)
        self.type_of_txn = type_of_txn
        self.amount = amount
        self.asset = asset
        self.user_name = user_name
        self.digital_signature = digital_signature
        self.privk = privk
        self.pubk = pubk

        if self.user_object is not None:
            self.privk = self.user_object.private_key
            self.pubk = self.user_object.public_key
            self.user_name = self.user_object.username
            self.__encrypt(user_object)
            self.__add_zkp()

    def __encrypt(self, user):
        # encryption of transaction.
        self.time = self.time  # encrypt(self.time, key=user.password, plaintext_is_hex=False, key_is_hex=False)
        self.type_of_txn = encrypt(self.type_of_txn, key=user.password, plaintext_is_hex=False, key_is_hex=False)
        self.amount = encrypt(self.amount, key=user.password, plaintext_is_hex=False, key_is_hex=False)
        self.asset = encrypt(self.asset.name, key=user.password, plaintext_is_hex=False, key_is_hex=False)
        self.user_name = self.user_object.username

    def to_dict(self):
        dict_ = {
            "time": self.time,
            "user_object": None,
            "user_name": self.user_name,
            "type_of_txn": self.type_of_txn,
            "amount": self.amount,
            "asset": self.asset,
            "digital_signature": self.digital_signature
        }
        return dict_

    def __add_zkp(self):
        x = str({
            "time": self.time,
            "user_name": self.user_name,
            "type_of_txn": self.type_of_txn,
            "amount": self.amount,
            "asset": self.asset
        })
        self.hash_ = sha256(x.encode('utf-8')).hexdigest()
        self.digital_signature = rsa_encrypt(self.hash_, self.privk.d, self.privk.n)  # encrypting the sha256 output


    # def add_zkp(self, username):
    #     with open(f'user_data\\{username}.json', 'r') as f:
    #         data = json.load(f)
    #         key = tuple_(data['public_key'])
    #     key = rsa.PublicKey(key[0], key[1])
    #     self.digital_signature = rsa.encrypt(self.hash_.encode(), key)
    #     self.digital_signature = base64.b64encode(self.digital_signature).decode('ascii')
    #
    #     return


    def verify_txn(self):
        x = str({
            "time": self.time,
            "user_name": self.user_name,
            "type_of_txn": self.type_of_txn,
            "amount": self.amount,
            "asset": self.asset
        })
        hash_ = sha256(x.encode('utf-8')).hexdigest()

        dig_sign_decr = rsa_decrypt(self.digital_signature, self.pubk.e, self.pubk.n)

        return dig_sign_decr == hash_


    @classmethod
    def from_dict(cls, dict_):
        with open(f'user_data\\{dict_["user_name"]}.json', 'r') as f:
            data = json.load(f)
            d = tuple_(data['public_key'])
            pubk = rsa.PublicKey(d[0], d[1])

        obj = Transaction(time=dict_["time"], user_name=dict_["user_name"], amount=dict_["amount"],
                          asset=dict_["asset"], type_of_txn=dict_["type_of_txn"], digital_signature=dict_['digital_signature'],
                          pubk = pubk)

        return obj


    def __str__(self):
        k = """[ "time" : {}, "user_name" : {}, "type_of_txn" :{}, "amount" :{}, "asset":{} ]""".format(self.time,
                                                                                                        self.user_name,
                                                                                                        self.type_of_txn,
                                                                                                        self.amount,
                                                                                                        self.asset)
        return k
