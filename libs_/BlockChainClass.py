"""
This file contains a block chain class.
"""
import pandas as pd

from .des_ import decrypt


class BlockChain():
    def __init__(self, user):
        self.blockchain = pd.read_json('block_chains\\{}_blockchain.json'.format(user.username)).T
        self.user = user
        return

    def append_block(self, block):
        if block.verify_block():
            self.blockchain = self.blockchain.append(block.to_dict(), ignore_index=True)
        else:
            print("wrong block. discarding it.")
            print(block.to_dict())

    def verify_whole_block_chain(self, verbose=False):
        """
        1. verify each transaction with zero knowledge proof.
        2. verify the chain--completed
        """
        flag = True
        for i in self.blockchain.index:
            if i != 0:
                if self.blockchain.loc[i - 1].hash != self.blockchain.loc[i].previous_hash:
                    flag = False
                    if verbose:
                        print(f'Wrong previous hash at block {i}.')
                if self.blockchain.loc[i - 1].timestamp > self.blockchain.loc[i].timestamp:
                    flag = False
                    if verbose:
                        print(f'Backdating at block {i}.')
            if not self.blockchain.loc[i].valid_proof():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
        return flag


    def push_to_json(self):
        self.blockchain.T.to_json('block_chains\\{}_blockchain.json'.format(self.user.username), indent=4)

    def show_my_transactions(self):
        if self.blockchain.empty:
            print("no transactions")
            return
        my_transactions = pd.DataFrame()
        for _, block in self.blockchain.iterrows():
            if self.user.username == block['transaction']['user_name']:
                txn = {}
                for i in block['transaction']:
                    if i == "time" or i == 'user_object' or i == 'user_name' or i == 'digital_signature':
                        txn[i] = block['transaction'][i]
                    else:
                        txn[i] = decrypt(block['transaction'][i], key=self.user.password, return_hex=False,
                                         key_is_hex=False)

                my_transactions = my_transactions.append(txn, ignore_index=True)

        if not my_transactions.empty:
            order_of_cols = ['time', 'type_of_txn', 'user_name', 'amount', 'asset']
            my_transactions = my_transactions[order_of_cols]
            print(my_transactions)
        else:
            print("no transactions associated with this user.")
        return
