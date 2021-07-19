'''
this .py file contains a class for the user and contains various methods.
'''
import datetime
import os
import rsa
import base64
import numpy as np

from .BlockChainClass import BlockChain
from .BlockClass import Block
from .TransactionClass import Transaction
from .des_ import encrypt, decrypt
from .utils import tuple_


import json
import pandas as pd
from hashlib import sha256
from .AssetClass import Asset


def add_to_for_sale_list(asset):
    df = pd.read_json('for_sale\\for_sale_assets.json').T
    df = df.append(asset.to_dict(), ignore_index=True)
    df.T.to_json('for_sale\\for_sale_assets.json', indent=4)
    return


class User():
    def __init__(self, tup):
        username = tup[0]
        password = tup[1]
        self.__load_data(username, password)
        if not self.__verify_password(password):
            raise Exception()


    def __str__(self):
        k = """
        "username":{},
        "password":{}
        """.format(self.username, self.password)
        return k


    def __load_data(self, username, password):
        with open(r"user_data\{}.json".format(username), 'r') as f:
            data = json.load(f)
            self.password_ = "b7b2ec16d69ed532781d8d4d4cf022ee"
            self.username = username
            self.password = password
            self.password_encr = data['password_encrypted']
            self.bankbalance = int(
                decrypt(data['bankbalance_encrypted'], key=self.password, return_hex=False, key_is_hex=False))
            self.assets = [Asset.decrypt(i, self) for i in data['assets_encrypted']]

            self.block = Block(self)
            self.blockchain = BlockChain(self)

            prv_key = tuple_(decrypt(data['private_key'], key = self.password, return_hex = False, key_is_hex = False))
            pub_key = tuple_(data['public_key'])

            self.private_key = rsa.PrivateKey(prv_key[0], prv_key[1], prv_key[2], prv_key[3], prv_key[4])
            self.public_key = rsa.PublicKey(pub_key[0], pub_key[1])

            # print(type(self.private_key), self.private_key)
            # print(type(self.public_key), self.public_key)


    def __verify_password(self, password):
        if sha256(password.encode('utf-8')).hexdigest() == self.password_encr:
            return True
        else:
            return False

    def commit_changes(self):
        with open(r"user_data\{}.json".format(self.username), 'w') as f:
            my_dict = {
                "username": self.username,
                "password_encrypted": self.password_encr,
                "bankbalance_encrypted": encrypt(self.bankbalance, key=self.password, key_is_hex=False,
                                                 plaintext_is_hex=False),
                "assets_encrypted": [x.encrypt(self) for x in self.assets],
                "private_key" : encrypt((self.private_key.n, self.private_key.e, self.private_key.d, self.private_key.p, self.private_key.q), self.password, plaintext_is_hex=False, key_is_hex=False),
                "public_key" : str((self.public_key.n, self.public_key.e))
            }
            json.dump(my_dict, f, indent=4)

        self.blockchain.push_to_json()

        with open('all_texts\\{}_text.json'.format(self.username), 'w') as f:
            empty = {}
            json.dump(empty, f, indent=4)
        return

    def add_txn_to_block(self, txn):
        if txn.verify_txn():
            if self.block.has_space():
                self.block.add_txn(txn)
                self.blockchain.append_block(self.block)
            else:
                self.block = Block(self)
                self.block.add_txn(txn)
                self.blockchain.append_block(self.block)
        else:
            print('transaction verification resulted false:')
            print(txn.to_dict())
        return

    def update_blockchain(self):
        df = pd.read_json('all_texts\\{}_text.json'.format(self.username)).T
        for _, txn in df.iterrows():
            txn_ = Transaction.from_dict(txn.to_dict())
            self.add_txn_to_block(txn_)
        return

    def show_my_assets(self):
        df = pd.DataFrame()
        for asset in self.assets:
            df = df.append(asset.to_dict(), ignore_index=True)
        if df.empty:
            print("no assets owned.")
        else:
            print(df)

    def show_my_balance(self):
        print(self.bankbalance)

    def buy(self):
        df = pd.read_json('for_sale\\for_sale_assets.json').T
        df.sort_values(by=['name'], inplace=True)
        df.index = np.arange(df.shape[0])
        if df.empty:
            print("no assets for sale")
            return

        print("the available assets are :")
        print(df)
        print("your balance is: {}".format(self.bankbalance))
        print("which one would you like to buy : ", end="")
        while True:
            index = int(input())
            x = df.iloc[index]
            # print("x", x)
            if int(x.value) > int(self.bankbalance):
                print("low balance, choose another one: ", end="")
            else:
                break

        asset = Asset(asset_name=x["name"], owner=x.owner, value=x.value)
        df.drop(index, axis=0, inplace=True)
        df.sort_values(by=['name'], inplace=True)
        df.index = np.arange(df.shape[0])
        df.T.to_json('for_sale\\for_sale_assets.json', indent=4)

        asset.owner = self.username
        self.assets.append(asset)
        self.bankbalance -= int(asset.value)

        time = datetime.datetime.now().timestamp()
        transaction = Transaction(time=time, user_object=self, amount=asset.value, asset=asset, type_of_txn='buy')

        # print('transaction.digital_signature', type(transaction.digital_signature), transaction.digital_signature)

        self.broadcast(transaction)
        self.add_txn_to_block(transaction)
        print('buying of {} is successful'.format(asset.name))
        self.show_my_balance()

    def sell(self):
        print("the available assets are: ")
        self.show_my_assets()
        if len(self.assets) == 0:
            print('no assets to sell.')
            return
        print("which one would you like to sell:", end="")
        index = int(input())

        asset = self.assets[index]
        self.assets.remove(asset)
        asset.owner = None
        add_to_for_sale_list(asset)

        self.bankbalance += asset.value

        time = datetime.datetime.now().timestamp()
        transaction = Transaction(time=time, user_object=self, amount=asset.value, asset=asset, type_of_txn='sell')

        self.broadcast(transaction)

        self.add_txn_to_block(transaction)

        print('selling of {} is successful'.format(asset.name))
        self.show_my_balance()

    def broadcast(self, txn):
        files = [i for i in os.listdir('all_texts') if i[-5:] == '.json']
        for i in files:
            if i[:5] != self.username:
                df = pd.read_json('all_texts\\' + i).T
                df = df.append(txn.to_dict(), ignore_index=True)
                df.T.to_json('all_texts\\' + i, indent=4)
        return
