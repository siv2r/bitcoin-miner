class Transaction:
    def __init__(self, txid, fee, weight, parents, ancesCnt=-1):
        """Object that stores a transaction.

        Args:
            txid (str): Hash of the transaction.
            fee (int): Miner's fee for including this transaction in a block.
            weight (int): Size of the transaction.
            parents (list): Dependencies for this transaction.
            ancesCnt (int, optional): Number of ancestors. Defaults to -1.
        """
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = [] if not parents else parents.split(';')
        self.ancestorCnt = ancesCnt

    def print(self):
        print(f"id: {self.txid}")
        print(f"fee: {self.fee}")
        print(f"weight: {self.weight}")
        print(f"parents: {self.parents}\n")

    def cntParent(self):
        return len(self.parents)
