from credentials import * # This is the file that has the credentials to
                          # connect to the database.
import mysql.connector
import re
import string

#####################################################################
# get_messages
#   Grab all the messages.
#####################################################################
def get_messages(cursor):
    cursor.execute('''
            SELECT id, content FROM message LIMIT 0, 1000;
        ''')
    messages = cursor.fetchall()

    for message in messages:
        line = message[1].decode('utf-8')
        words = line.split()

        # Insert into the tables
        for word in words:
            cursor.execute('''
                    INSERT INTO keyword SET text = %s
                ''', (word,))
            rowId = cursor.lastrowid

            cursor.execute('''
                    INSERT INTO message_keyword SET message_id = %s, keyword_id = %s 
                ''', (message[0], rowId))

    return

#####################################################################
# main
#   Driver program.
#####################################################################
def main():
    # Grab the credentials for the database.
    global user
    global password
    global host
    global database

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()

    # Run all the execution statements.
    try:
        get_messages(cursor)
    finally:
        cnx.close()
    return

if __name__ == '__main__':
    main()