from tron_explorer.explore import Explore
explore = Explore()

# getting the latest block
last_block = explore.get_latest_block(properties=["number", "hash", "confirmed"])
print(last_block)

# getting a specific block
block = explore.get_block(45986120)
print(block.size)

# getting a list of blocks
df_blocks = explore.get_block_list(start_timestamp=1668537846000, end_timestamp=1668539846000)
print(df_blocks["block_reward"])