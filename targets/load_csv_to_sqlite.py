import csv
import sql as s
import settings
h = s.SalesDB()
h.open()

with open('github_top_users_target_list.csv','r') as fin:
	dr = csv.DictReader(fin) 
	to_db = [(i['first_name'], i['last_name'], i['email'], i['github_project_name'], i['alternate_dev_name'], i['alternate_dev_21_profile']) for i in dr]

for x in to_db:
	target_id = h.add_target(x[0], x[1], x[2], None, None)
	parameters = {'github_project_name': x[3], 'alternate_dev_name': x[4], 'alternate_dev_21_profile': x[5]}
	h.add_campaign_personalization(target_id, 1, parameters)
	print(target_id)

print('Finished')