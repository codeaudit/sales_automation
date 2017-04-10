import sqlite3
import time
import json

import utils
import settings

class SalesDB(object):
	def open(self):
		self.conn = sqlite3.connect(settings.DB)
		self.conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
		self.c = self.conn.cursor()


	def save(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

	def setup_tables(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS targets (
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			created INTEGER NOT NULL,
			last_modified INTEGER NOT NULL,
			first_name TEXT NOT NULL,
			last_name TEXT,
			email TEXT NOT NULL,
			other_contact_info TEXT,
			funnel_state INTEGER NOT NULL,
			notes TEXT,
			value REAL
		)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS campaign_personalization (
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			target_id INTEGER NOT NULL, 
		    campaign_id INTEGER NOT NULL,
		   	parameters TEXT NOT NULL,
			    FOREIGN KEY (target_id) REFERENCES targets(id),
			    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
		)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			created INTEGER NOT NULL,
			last_modified INTEGER NOT NULL,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			start INTEGER,
			finish INTEGER,
			targets TEXT NOT NULL,
			hit_targets TEXT,
			status INTEGER NOT NULL,
			response_rate REAL,
			win_rate REAL,
			notes TEXT,
			value REAL
		)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS messages (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			message_id TEXT NOT NULL,
			thread_id TEXT,
			campaign_id INTEGER NOT NULL,
			status INTEGER NOT NULL,
		    sent INTEGER,
		    recipient TEXT NOT NULL,
		    sender TEXT NOT NULL,
		    subject TEXT NOT NULL,
		    body TEXT NOT NULL,
		    response INTEGER,
			    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
			    FOREIGN KEY (response) REFERENCES messages(id)
		)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS templates (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			created INTEGER NOT NULL,
			last_modified INTEGER NOT NULL,
			campaign_id INTEGER NOT NULL, 
		    subject TEXT NOT NULL,
		    body TEXT NOT NULL,
		    attachments TEXT,
			    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
		)''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS statistics (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			time_stamp INTEGER NOT NULL,
			response_rate REAL NOT NULL,
			interest_rate REAL NOT NULL, 
		    win_rate REAL NOT NULL,
		    best_campaign INTEGER NOT NULL,
		    best_template INTEGER NOT NULL,
		    most_valuable_campaign INTEGER NOT NULL,
		    most_valuable_target INTEGER NOT NULL,
			    FOREIGN KEY (best_campaign) REFERENCES campaigns(id),
			    FOREIGN KEY (best_template) REFERENCES templates(id),
			    FOREIGN KEY (most_valuable_campaign) REFERENCES campaigns(id),
			    FOREIGN KEY (most_valuable_target) REFERENCES targets(id)
		)''')

	def add_target(self, first_name, last_name, email, other_contact_info, notes, multiple=False):
		now = time.time()
		self.c.execute("INSERT INTO targets VALUES (NULL,?,?,?,?,?,?,?,?,?)", (now, now, first_name, last_name, email, other_contact_info, 0, notes, 0.00))
		if not multiple:
			self.save()

		return self.c.lastrowid

	def add_campaign_personalization(self, target_id, campaign_id, parameters, multiple=False):
		self.c.execute("INSERT INTO campaign_personalization VALUES (NULL,?,?,?)", (target_id, campaign_id, json.dumps(parameters)))
		if not multiple:
			self.save()

		return self.c.lastrowid	

	def add_campaign(self, name, description, targets, notes, target_params):
		now = time.time()
		self.c.execute("INSERT INTO campaigns VALUES (NULL,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?)", (now, now, name, description, None, None, targets, None, 0, 0.00, 0.00, notes, 0.00))
		self.save()

		return self.c.lastrowid

	def add_message(self, message_id, thread_id, campaign_id, sent, recipient, sender, subject, body):
		self.c.execute("INSERT INTO messages VALUES (NULL,?,?,?,?,?,?,?,?,?,?)", (message_id, thread_id, campaign_id, 0, sent, recipient, sender, subject, body, None))
		self.save()

		return self.c.lastrowid

	def add_template(self, campaign_id, subject, body, attachments):
		now = time.time()
		self.c.execute("INSERT INTO templates VALUES (NULL,?,?,?,?,?,?)", (now, now, campaign_id, subject, body, attachments))
		self.save()

		return self.c.lastrowid

	def get_template(self, campaign_id):
		self.c.execute("SELECT * FROM templates WHERE campaign_id = ?", (campaign_id,))
		template = self.c.fetchone()
		return template

	def get_target(self, target_id):
		self.c.execute("SELECT * FROM targets WHERE id = ?", (target_id,))
		target_row = self.c.fetchone()
		return target_row

	def get_target_personalization(self, target_id, campaign_id):
		self.c.execute("SELECT * FROM campaign_personalization WHERE target_id = ? AND campaign_id = ?", (target_id, campaign_id))
		campaign_personalization_row = json.loads(self.c.fetchone()['parameters'])

		return campaign_personalization_row

	def set_message_status(self, message_id, status):
		"""
		status
			0 DRAFT
			1 SENT
			2 INACTIVE
		"""
		self.c.execute("UPDATE messages SET status = ? WHERE id = ?", (status, message_id))
		self.save()

	def set_message_thread(self, message_id, thread_id):
		self.c.execute("UPDATE messages SET thread_id = ? WHERE id = ?", (thread_id, message_id))
		self.save()
