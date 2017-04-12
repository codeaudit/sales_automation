import pandas as pd
import requests
import subprocess
import json

pd.set_option('display.width', 200)

a = open('github_top1000_users_raw.json', 'r')
df = pd.read_json(a)
a.close()

alternate_dev_name = 'TJ Holowaychuk'
alternate_dev_21_profile = 'tj'

good_df = df.dropna(subset=['email'])
good_df = good_df.dropna(subset=['name'])


output_list = []

for index, row in good_df.iterrows():
	name_array = row['name'].split(' ')
	first_name = name_array[0]
	try:
		last_name = name_array[1]
	except: 
		last_name = None

	email = row['email']

	repo_url = row['repos_url']

	try:
		a = subprocess.run('curl -u tgpski:############################ %s' % repo_url, shell=True, stdout=subprocess.PIPE)
	except:
		break
	json_out = json.loads(a.stdout.decode())

	best = {'stars': 0, 'name': 'None'}
	for x in json_out:
		if x['stargazers_count'] > best['stars']:
			best['stars'] = x['stargazers_count']
			best['name'] = x['name']

	github_project_name = best['name']

	print(first_name, last_name, email, github_project_name, alternate_dev_name, alternate_dev_21_profile)

	output_list.append([first_name, last_name, email, github_project_name.title(), alternate_dev_name, alternate_dev_21_profile])


output_df = pd.DataFrame(output_list, columns=['first_name', 'last_name', 'email', 'github_project_name', 'alternate_dev_name', 'alternate_dev_21_profile'])

output_df.to_csv('github_top_users_target_list.csv', sep=',', encoding='utf-8')
