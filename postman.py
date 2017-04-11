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
		template = self.handle.get_template(campaign_id)
		subject_template = Template(template['subject'])
		body_template = Template(template['body'])

		target_row = self.handle.get_target(target_id)
		target_personalization_row = self.handle.get_target_personalization(target_id, campaign_id)

		draft = self.client.drafts.create()

		draft.to = [{
			'name': target_row['first_name'],
			'email': target_row['email']
		}]

		draft.cc = [{
			'name': settings.CC_NAME,
			'email': settings.CC_EMAIL
		}]

		draft.bcc = [{
			'name': 'salesforceIQ',
			'email': settings.SALESFORCEIQ_EMAIL
		}]
		
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

	def send_draft(self, message_id):
		utils.print_magenta('Send draft')
		draft = self.client.drafts.find(message_id)
		utils.print_pretty(draft)

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
