from classes.transaction import Transaction
import csv

class Mempool():
    def __init__(self, fileName, txns=list(), eqTxns=list(), vis=set()):
        """Mempool constructor.

        Args:
            fileName (str): Name of the input file.
            txns (list, optional): List of all transactions from input file. Defaults to list().
            eqTxns (list, optional): List of equivalent transactions that will be calculated. Defaults to list().
            vis (set, optional): Used when performing DFS. Defaults to set().
        """
        self.fileName = fileName
        self.txns = list()
        self.eqTxns = list()
        self.visitedTxids = set()

    def parse_csv(self):
        """Parses the input file and fills the transactions into a list."""
        with open(self.fileName, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                newTxn = Transaction(line['tx_id'], line['fee'], line['weight'], line['parents'])
                self.txns.append(newTxn)

    def createOneEqTxn(self, tx):
        """Creates an equivalent transaction for the given transaction by visiting its ancestors (via DFS) and adding their weight and fees into one.

        Args:
            tx (Transaction): Transaction whose equivalent we need.

        Returns:
            Transaction: Calculated equivalent transaction.
        """
        self.visitedTxids.add(tx.txid)

        if tx.cntParent() == 0:
            return tx
        else:
            eqTxnId, eqTxnFee, eqTxnWeight = '', 0, 0
            for parTxid in tx.parents:
                if parTxid in self.visitedTxids:
                    continue

                parIdx = self.findTxnIndex(parTxid)
                par = self.txns[parIdx]
                parEqTxn = self.createOneEqTxn(par)
                eqTxnId = parEqTxn.txid if eqTxnId == '' else eqTxnId + '\n' + parEqTxn.txid
                eqTxnFee += parEqTxn.fee
                eqTxnWeight += parEqTxn.weight

            eqTxnId = tx.txid if eqTxnId == '' else eqTxnId + '\n' + tx.txid
            eqTxnFee += tx.fee
            eqTxnWeight += tx.weight

            return Transaction(eqTxnId, eqTxnFee, eqTxnWeight, '')

    def createEqTxnPool(self):
        """Creates a new pool of equivalent transactions by looping through all the input transactions."""
        self.visitedTxids = set()

        for tx in self.txns:
            if tx.txid in self.visitedTxids:
                continue

            eqTxn = self.createOneEqTxn(tx)
            self.eqTxns.append(eqTxn)

    def findTxnIndex(self, txid):
        for i in range(len(self.txns)):
            if self.txns[i].txid == txid:
                return i
        raise Exception(f'Transaction id: {txid} not present in Mempool.txns')

    def findEqTxnIndex(self, txid):
        for i in range(len(self.eqTxns)):
            currEqTxnIds = self.eqTxns[i].txid.split('\n')
            if txid in currEqTxnIds:
                return i
        raise Exception(f'Transaction id: {txid} not present in Mempool.eqTxns')

    def AncestorCnt(self, tx):
        """Calculates the number of ancestors that a given transaction has.

        Args:
            tx (Transaction): Input transaction.

        Returns:
            int: Number of ancestor transactions present.
        """
        self.visitedTxids.add(tx.txid)

        if tx.cntParent() == 0:
            return 0
        else:
            ancestors = 0
            for parId in tx.parents:
                if parId in self.visitedTxids:
                    continue
                parIdx = self.findTxnIndex(parId)
                par = self.txns[parIdx]
                ancestors += self.AncestorCnt(par) + 1
            return ancestors

    def calcAllAncestorCnt(self):
        """Calculates ancestors for all available transactions."""
        for tx in self.txns:
            self.visitedTxids = set()
            tx.ancestorCnt = self.AncestorCnt(tx)

    def print(self):
        record = 0
        for tx in self.txns:
            record += 1
            print(f"Record {record}:")
            tx.print()
