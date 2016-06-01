import mysql.connector
import string
from credentials import *
import re

def remove_garbage(msg):

	# replace ' to `
	msg = msg.replace("'","`")
	# replace \ to the word "back-slash"
	msg = msg.replace("\\", "back-slash")
	# remove some punctuation
	msg = re.sub(r"(\w*)[.,:;]([\s\n])", r"\1\2", msg)
	# remove urls and emails
	msg = re.sub(r"((?:http:\/\/|ftp:\/\/|https:\/\/|\w+@)\S*)[ ]?|([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?[ ]?", "", msg)
	return msg

def parse_messages(initial, final):

	# parse messages that were not flag as processed yet
	global user
	global password
	global host
	global database

	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

	query = ("SELECT id, content as msg from message where processed = 0 and id between %s and %s" % (initial, final))
	global cursor
	cursor = cnx.cursor()
	cursor.execute(query)

	data = cursor.fetchall()
	cnx.close()

	for row in data:
		analyze_message(remove_garbage(row[1]), row[0])
		print "'Working message: %s" % (row[0])


def analyze_message(content, msg_id):

	keywords = string.split(content)

	global user
	global password
	global host
	global database
	global cursor

	cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
	cursor = cnx.cursor();
	
	# flag message as processed
        flag_message = "UPDATE message set processed = 1 where id = %s" % (msg_id)
        try:
                cursor.execute(flag_message)
        except mysql.connector.Error as err:
  		print("Something went wrong: {}".format(err))
                print flag_message

	for (keyword) in keywords:

		keyword_id = 0

		# check if the keyword is already inside the database
		query = ("SELECT id from keyword where text = '%s'" % (keyword))
		
		cursor = cnx.cursor()
		cursor.execute(query)

		for (id) in cursor:
			keyword_id = id[0]

		if keyword_id == 0:

			# insert new keyword
			add_keyword = "INSERT INTO keyword (text) VALUES ('%s')" % (keyword)
			try:
				cursor.execute(add_keyword)
				keyword_id = cursor.lastrowid
				# print "%s" % (keyword_id)
			except:
				print "%s" % (add_keyword)

		# relate message with keyword
		print keyword
		# print msg_id
		# print int(keyword_id)

		add_message_keyword = "INSERT INTO message_keyword (message_id, keyword_id) values ('%s', '%s')" % (msg_id, keyword_id)
		try:
			cursor.execute(add_message_keyword)
		except:
			print "Error: %s" % (add_message_keyword)


	cnx.commit()
	cnx.close()



