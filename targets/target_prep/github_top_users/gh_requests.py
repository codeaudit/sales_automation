import requests

r = requests.get('https://api.github.com/users/sindresorhus/repos')
json_out = r.json()

best = {'stars': 0, 'name': 'None'}

for x in json_out:
	if x['stargazers_count'] > best['stars']:
		best['stars'] = x['stargazers_count']
		best['name'] = x['name']

print(best)	