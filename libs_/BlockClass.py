import pandas as pd
import hashlib
import datetime
from .des_ import encrypt


class Block():
    def __init__(self, user):
        self.user = user
        self.txn = None
        self.timestamp = None
        self.previous_hash = None
        self.lotxns = None
        self.proof = None
        self.hash = None
        return

    def has_space(self):
        if self.txn is None:
            return True
        else:
            return False

    def add_txn(self, txn):
        if txn.verify_txn():
            self.txn = txn
            self.timestamp = txn.time
            df = self.user.blockchain.blockchain  # pd.read_json('block_chains\\{}_blockchain.json'.format(self.user.username)).T
            if not df.empty:
                self.previous_hash = df.iloc[-1]['hash']
            else:
                self.previous_hash = "0001"

            if not self.has_space():
                self.mine_block()


    def calculate_lotxns(self):
        return encrypt(hashlib.sha256(
            (self.previous_hash + str(self.txn.to_dict()) + str(self.timestamp)).encode("utf-8")).hexdigest())

    def mine_block(self):
        self.lotxns = self.calculate_lotxns()
        self.proof = 0
        while not self.valid_proof():
            self.proof += 1

    def valid_proof(self):
        guess = f'{self.lotxns}{self.proof}{self.previous_hash}'.encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()
        if guess_hash[:3] == "000":
            self.hash = guess_hash
            return True
        else:
            return False

    def to_dict(self):
        dict_ = {
            "transaction": self.txn.to_dict(),
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "proof": self.proof
        }
        return dict_

    def __str__(self):
        k = self.to_dict()
        return str(k)

    def verify_block(self):
        # some code need to be written here.
        return True
