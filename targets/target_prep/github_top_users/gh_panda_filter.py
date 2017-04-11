import pandas as pd

pd.set_option('display.width', 500)

a = open('github_top1000_users_raw.json', 'r')
df = pd.read_json(a)
a.close()

good_df = df.dropna(subset=['email'])

