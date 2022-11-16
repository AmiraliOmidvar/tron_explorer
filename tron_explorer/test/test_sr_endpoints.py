from tron_explorer.explore import Explore
explore = Explore()

# get a single sr
sr = explore.get_sr("TTxrh32VJveqiYRwbLEX2wLTMFCfbpAUQj")
print(sr.name, sr.url)

# get list of all sr (super representatives, sr_partners, sr_candidates) check doc for more info
df_sr_all = explore.get_sr_list()
print(df_sr_all)

# get list of sr_candidates
df_sr_candid = explore.get_sr_list(sr_type="sr_candidate")
print(df_sr_candid)
