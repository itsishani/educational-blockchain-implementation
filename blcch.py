"""
BLOCKCHAIN SIMULATION IMPLEMENTATION
Features:
- Cryptographic block chaining with SHA-256
- Proof-of-Work consensus mechanism
- Transaction pooling and block mining
- Chain validation and tamper detection
"""

import datetime
import hashlib
import json

# =====================================================================
# BLOCK CLASS IMPLEMENTATION
# =====================================================================

class Block:
    """Represents a single block in the blockchain containing transaction data."""
    
    # -------------------------
    # INITIALIZATION & MINING
    # -------------------------
    def __init__(self, index, timestamp, transactions, previous_hash):
        """
        Initialize a new block with cryptographic mining.
        
        Args:
            index (int): Position in the blockchain
            timestamp (datetime): Creation time of the block
            transactions (list): Data records contained in the block
            previous_hash (str): Hash of the previous block in chain
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions.copy()  # Prevent reference issues
        self.previous_hash = previous_hash
        self.nonce = 0  # Cryptographic puzzle solution
        self.hash = self.mine_block()  # Set through mining process

    # -------------------------
    # CRYPTOGRAPHIC OPERATIONS
    # -------------------------
    def calculate_hash(self):
        """Generate SHA-256 hash of block contents using JSON serialization."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self):
        """
        Perform proof-of-work to create valid block hash.
        
        Mining Process:
        1. Continuously calculates block hash
        2. Increments nonce until hash meets target difficulty
        3. Uses simple difficulty target of two leading zeros ('00')
        """
        target = "00"  # Mining difficulty setting
        self.hash = self.calculate_hash()
        
        # Proof-of-work computation loop
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

# =====================================================================
# BLOCKCHAIN CLASS IMPLEMENTATION
# =====================================================================

class Blockchain:
    """Manages the complete blockchain network and operations."""
    
    # -------------------------
    # CHAIN INITIALIZATION
    # -------------------------
    def __init__(self):
        """Initialize blockchain with genesis block and empty transaction pool."""
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []  # Temporary transaction storage

    def create_genesis_block(self):
        """Create the genesis block with hardcoded initial values."""
        return Block(
            index=0,
            timestamp=datetime.datetime.now(),
            transactions=[],
            previous_hash="0"  # Initial hash value
        )

    # -------------------------
    # TRANSACTION MANAGEMENT
    # -------------------------
    def add_transaction(self, transaction):
        """
        Add new transaction to pending pool.
        
        Args:
            transaction (str): Transaction data to record
        """
        self.pending_transactions.append(transaction)

    # -------------------------
    # BLOCK CREATION & MINING
    # -------------------------
    def mine_pending_transactions(self):
        """
        Create new block with pending transactions and add to chain.
        
        Process:
        1. Checks for pending transactions
        2. Creates new block with current transactions
        3. Resets pending transaction pool
        """
        if not self.pending_transactions:
            return False  # No transactions to mine

        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.datetime.now(),
            transactions=self.pending_transactions,
            previous_hash=self.chain[-1].hash
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear transaction pool
        return True

    # -------------------------
    # CHAIN VALIDATION
    # -------------------------
    def validate_chain(self):
        """
        Validate complete blockchain integrity.
        
        Checks:
        1. Genesis block structure
        2. Cryptographic hash links between blocks
        3. Proof-of-work compliance
        4. Transaction data immutability
        
        Returns:
            bool: True if chain is valid, False if tampering detected
        """
        # Validate genesis block
        genesis = self.chain[0]
        if (genesis.index != 0 or 
            genesis.previous_hash != "0" or 
            genesis.hash != genesis.calculate_hash() or 
            not genesis.hash.startswith("00")):
            return False

        # Validate subsequent blocks
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Current block validation
            if current.hash != current.calculate_hash():
                return False  # Tampered block content
                
            # Chain linkage validation
            if current.previous_hash != previous.hash:
                return False  # Broken chain link
                
            # Proof-of-work validation
            if not current.hash.startswith("00"):
                return False  # Invalid mining proof

        return True

    # -------------------------
    # CHAIN VISUALIZATION
    # -------------------------
    def print_chain(self):
        """Display formatted blockchain contents with block details."""
        for block in self.chain:
            print(f"\nBlock {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Current Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 60)

# =====================================================================
# TESTING IMPLEMENTATION
# =====================================================================

if __name__ == "__main__":
    # Initialize blockchain network
    bc = Blockchain()

    # TEST CASE 1: Normal operation
    print("\n*** TESTING NORMAL BLOCKCHAIN OPERATION ***")
    
    # Add initial transactions
    bc.add_transaction("Alice pays Bob 2 BTC")
    bc.add_transaction("Bob pays Charlie 1 BTC")
    bc.mine_pending_transactions()  # Mine block 1

    # Add subsequent transactions
    bc.add_transaction("Charlie pays Dave 0.5 BTC")
    bc.mine_pending_transactions()  # Mine block 2

    # Display initial chain state
    print("\nINITIAL BLOCKCHAIN STATE:")
    bc.print_chain()
    
    # Validate chain integrity
    print("\nInitial Chain Validation:", bc.validate_chain())

    # TEST CASE 2: Tamper detection
    print("\n*** TESTING TAMPER DETECTION ***")
    
    # Attempt to alter transaction history
    try:
        print("\nTampering with Block 1 transactions...")
        bc.chain[1].transactions[0] = "Alice pays Bob 10 BTC"
    except AttributeError as e:
        print(f"Error: {e}")

    # Display modified chain state
    print("\nMODIFIED BLOCKCHAIN STATE:")
    bc.print_chain()
    
    # Re-validate after tampering
    print("\nPost-Tampering Validation:", bc.validate_chain())
