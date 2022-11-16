from tron_explorer.explore import Explore
import matplotlib.pyplot as plt
import pandas as pd

explore = Explore()

# getting a single account data
account = explore.get_account("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", properties=["address", "balance"])
print(account.balance)

account = explore.get_account("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(account.number_of_transactions)

# get a list of accounts
df_accounts = explore.get_account_list(count=200)
print(df_accounts["number_of_transactions"].mean())

df_accounts = explore.get_account_list(save_live=True, sort="power", count=10
                                       , properties=explore.get_account_properties())
print(df_accounts["power"])

# get analysis for accounts
df_balance_history = explore.get_account_analysis("balance", "TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb")
pd.to_numeric(df_balance_history["usdt_amount"]).plot()
plt.show()

df_energy_history = explore.get_account_analysis("energy", "TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb"
                                                 , start_timestamp=1668439846000)
print(df_energy_history)