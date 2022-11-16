from tron_explorer.explore import Explore
explore = Explore()

# get single transaction
transaction = explore.get_transaction("2f12d1470965a0b439a0b7f50a0c588f5ed7267cd99857489b32b19c578c969f")
print(transaction)

# get transactions that are in a specific block
df_block_transactions = explore.get_transaction_list_block("46012029", save_live=True, save_path="account_transactions/")

# get transactions related to an account
df_account_transactions = explore.get_transaction_list_account("TRHcKhF2NZHnUSWtnB5bAoueSgifwuEsAf"
                                                             , properties=["from_address", "to_address"])
print(df_account_transactions)

# get transaction list in whole blockchain
df_blockchain_transactions = explore.get_transaction_list_blockchain(start_timestamp=1668613534000)
print(df_blockchain_transactions)