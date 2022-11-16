from tron_explorer.explore import Explore
explore = Explore()

# get single trc10 token
trc10_token = explore.get_trc10_token("0")
print(trc10_token)

# get single trc20 token
trc20_token = explore.get_trc20_token("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(trc20_token.supply)

# get list of token
df_token_list = explore.get_token_list(properties=["market_cap", "gain"])
print(df_token_list)


