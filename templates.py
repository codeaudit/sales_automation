import sql
import settings
import utils
import yaml

class InsideSalesTemplates(object):
	def __init__(self):
		self.h = sql.SalesDB()
		self.h.open()

	def close(self):
		self.h.close()

	def add_template(self, yaml_file, campaign_id):
		stream = open(yaml_file, 'r')
		yaml_dict = yaml.load(stream)
		stream.close()
		body = yaml_dict['body'].replace("\n", "<br/>")
		template_id = self.h.add_template(campaign_id, yaml_dict['subject'], body, None)		

		return template_id

	def list_templates(self):
