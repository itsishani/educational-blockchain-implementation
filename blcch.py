import datetime
import hashlib
import json


class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.mine_block()

    def calculate_hash(self):
        """Calculates the SHA-256 hash of the block based on its contents."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self):
        """Mines the block by finding a hash that starts with '00'."""
        target = "00" 
        self.hash = self.calculate_hash()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

class Blockchain:
    """Manages the chain of blocks and its operations."""
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        """Creates the first block in the chain with default values."""
        return Block(0, datetime.datetime.now(), [], "0")

    def add_transaction(self, transaction):
        """Adds a new transaction to the list of pending transactions."""
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        """Creates a new block with all pending transactions and adds it to the chain."""
        if not self.pending_transactions:
            return False
        
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), datetime.datetime.now(), 
                          self.pending_transactions, last_block.hash)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def validate_chain(self):
        """Validates the integrity of the blockchain."""
        if len(self.chain) < 1:
            return False
        
        genesis = self.chain[0]
        if (genesis.index != 0 or 
            genesis.previous_hash != "0" or 
            genesis.hash != genesis.calculate_hash() or 
            not genesis.hash.startswith("00")):
            return False
       
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if (current_block.hash != current_block.calculate_hash() or 
                not current_block.hash.startswith("00") or 
                current_block.previous_hash != previous_block.hash):
                return False
        return True

    def print_chain(self):
        """Prints the details of each block in the chain."""
        for block in self.chain:
            print(f"Block {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 20)

 
if __name__ == "__main__":
    bc = Blockchain()

    
    bc.add_transaction("Alice pays Bob 2 BTC")
    bc.add_transaction("Bob pays Charlie 1 BTC")
    bc.mine_pending_transactions()

    bc.add_transaction("Charlie pays Dave 0.5 BTC")
    bc.mine_pending_transactions()

    
    print("Initial Blockchain:")
    bc.print_chain()

    
    print("Is the blockchain valid?", bc.validate_chain())

    
    print("\nTampering with the data...")
    bc.chain[1].transactions[0] = "Alice pays Bob 10 BTC"  # Alter a transaction

   
    print("Blockchain after tampering:")
    bc.print_chain()

    
    print("Is the blockchain valid after tampering?", bc.validate_chain())
