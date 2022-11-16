# Tron Explorer

Tron explorer is a python wrapper for tronscan.org REST API. with the help of Tron explore get most of the data available on tronscan.org without pagination.

## Features
Getting data for blocks, accounts, proposals, SRs, smart contracts, tokens and transactions from start to current state of blockchain with one request.

## Installation

Use pip to install tron_explore.

```bash
pip install tron_explore
```

## Usage

```python
from tron_explore.explore import Explore

explore = Explore()

# returns the latest block data
explore.get_latest_block()

# prints specified properties of the latest block
latest_block = explore.get_latest_block(properties = ["number", "hash"])
print(latest_block.number, latest_block.hash)

# prints all the available properties of block type data
print(get_block_properties())

# get a specific block
# when no property is mentioned all of them will be returned
block = explore.get_block(block_number)
print(block.block_reward)

# get a list of blocks with specified properties and save them to a csv file
# as being downloaded (the csv file will be in blocks/query.csv)
df_block = explore.get_block_list(count = 20000, save_live=True, save_path = "blocks"
                                  ,properties=["number", "hash", "size", "block_reward"])

# after download is completed df_blocks will be a pandas dataframe with
# ["number", "hash", "size", "block_reward"] columns and 20000 rows.
```
for more examples and info on other data types you can check out the test package which has a full demonstration of all methods, or you can look up the doc.

## Documentation

you can find tron_explore doc here.

## Contributing

Any contribution is welcome. please open an issue to discuss changes or improvements.

## License

MIT