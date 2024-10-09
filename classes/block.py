from classes.transaction import Transaction
from classes.mempool import Mempool

class Block():
    def __init__(self, maxWeight=float('inf'), txns=list(), weight=0, fee=0, vis=set()):
        """Constructor for Block class.

        Args:
            maxWeight (int, optional): Maximum weight this block can have. Defaults to float('inf').
            txns (list, optional): Transactions in this block. Defaults to [].
            weight (int, optional): Sum of weight of every transaction present. Defaults to 0.
            fee (int, optional): Sum of fee of every transaction present. Defaults to 0.
            vis (set, optional): Used for marking nodes in DFS. Defaults to set().
        """
        self.txns = txns
        self.weight = weight
        self.fee = fee
        self.visitedEqTxnIds = vis
        self.maxWeight = maxWeight

    def addEqTxn(self, eqTxn, mempool):
        """Adds an equivalent transaction to this block.

        Args:
            eqTxn (Transaction): Combining transaction with its ancestors into a single transaction.
            mempool (Mempool): Parsed inputs.
        """
        # Mark the eqTxn as visited
        self.visitedEqTxnIds.add(eqTxn.txid)
        eqTxnIds = eqTxn.txid.split('\n')
        for txid in eqTxnIds:
            # Get the txn from its id
            txnIdx = mempool.findTxnIndex(txid)
            tx = mempool.txns[txnIdx]

            for parTxid in tx.parents:
                parEqTxnIdx = mempool.findEqTxnIndex(parTxid)
                parEqTxn = mempool.eqTxns[parEqTxnIdx]
                if parEqTxn.txid in self.visitedEqTxnIds:
                    continue
                self.addEqTxn(parEqTxn, mempool)

        # Add current eqTxn
        self.txns.append(eqTxn)
        self.weight += eqTxn.weight
        self.fee += eqTxn.fee

    def selectOptEqTxns(self, mempool):
        """Loops through all the equivalent transactions and adds them sequentially along with their parents. 
        Note: The equivalent transaction list must be sorted before using this function.

        Args:
            mempool (Mempool): Parsed input.
        """
        # Mark all ids as not visited
        self.visitedTxnIds = set()

        for eqTxn in mempool.eqTxns:
            if eqTxn.txid in self.visitedEqTxnIds:
                continue

            if eqTxn.weight + self.weight <= self.maxWeight:
                self.addEqTxn(eqTxn, mempool)

    def print(self):
        print("Transactions: {}".format(self.txns))
        print("Fee: {}".format(self.fee))
        print("Weight: {}\n".format(self.weight))

    def createTxt(self):
        """Creates the block.txt file."""
        with open('block.txt', 'w') as file_handle:
            for tx in self.txns:
                file_handle.write('{}\n'.format(tx.txid))
