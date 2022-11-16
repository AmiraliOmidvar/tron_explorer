from tron_explorer.explore import Explore
explore = Explore()

# get single a smart contract
contract = explore.get_smart_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(contract)

# get list of contracts
df_contracts = explore.get_smart_contract_list_blockchain(start_timestamp=1660602534000
                                                          , count=100, properties=["contract_address", "balance"])
print(df_contracts)