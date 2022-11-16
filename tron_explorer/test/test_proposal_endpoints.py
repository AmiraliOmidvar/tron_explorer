from tron_explorer.explore import Explore
explore = Explore()

# get proposals on network
df_proposals = explore.get_list_proposals()

# get network parameters
parameters = explore.get_list_network_parameters()