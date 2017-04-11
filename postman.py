from string import Template
import json

import sql
from nylas import APIClient
import settings
import utils

class Postman(object):

	def __init__(self):
		self.client = APIClient(settings.APP_ID, settings.APP_SECRET, settings.TOKEN)
		self.handle = sql.SalesDB()
		self.handle.open()


	def create_draft(self, campaign_id, target_id, template_id):
		template = self.handle.get_template(template_id)
		subject_template = Template(template['subject'])
		body_template = Template(template['body'])

		target_row = self.handle.get_target(target_id)
		target_personalization_row = self.handle.get_target_personalization(target_id, campaign_id)

		draft = self.client.drafts.create()

		draft.to = [{
			'name': target_row['first_name'],
			'email': target_row['email']
		}]

		# draft.cc = [{
		# 	'name': settings.CC_NAME,
		# 	'email': settings.CC_EMAIL
		# }]

		# draft.bcc = [{
		# 	'name': 'salesforceIQ',
		# 	'email': settings.SALESFORCEIQ_EMAIL
		# }]
		
		draft.subject = subject_template.substitute(target_personalization_row)
		draft.body = body_template.substitute({**target_row, **target_personalization_row})
		draft.save()

		print(' ')
		utils.print_magenta('Draft Message to %s' % target_row['email'])
		utils.print_green('message id: ' + draft.id)
		utils.print_pretty(draft.to)
		utils.print_pretty(draft.subject)
		utils.print_pretty(draft.body)
		print(' ')

		self.handle.add_message(draft.id, None, campaign_id, None, draft.to[0]['email'], settings.SENDER_EMAIL, draft.subject, draft.body)

		return draft.id

	def send_draft(self, message_id, bypass=False):
		utils.print_magenta('Send draft')
		draft = self.client.drafts.find(message_id)
		utils.print_pretty(draft)

		if bypass:
			message = draft.send()
			self.handle.set_message_status(message_id, 1)
			self.handle.set_message_thread(message_id, message['thread_id'])
			print(' ')
			utils.print_red('MESSAGE SENT')
			utils.print_magenta('thread id: ' + message['thread_id'])
			print(' ')
			return message['thread_id']

		send = input("Send draft? (y/n) ")

		if send == 'y' or send == 'Y':
			message = draft.send()
			self.handle.set_message_status(message_id, 1)
			self.handle.set_message_thread(message_id, message['thread_id'])
			print(' ')
			utils.print_red('MESSAGE SENT')
			utils.print_magenta('thread id: ' + message['thread_id'])
			print(' ')
		else:
			utils.print_red('Draft not sent.')

	def generate_campaign_drafts(self, campaign_id, template_id):
		target_id_list = self.handle.get_target_list(campaign_id)

		draft_id_list = []

		for x in target_id_list:
			id_out = self.create_draft(campaign_id, x['id'], template_id)
			draft_id_list.append(id_out)

		return draft_id_list

	def send_campaign_drafts(self, message_id_list):
		thread_ids = []
		for x in message_id_list:
			thread_id = self.send_draft(x, bypass=True)
			thread_ids.append(thread_id)

		return thread_ids
