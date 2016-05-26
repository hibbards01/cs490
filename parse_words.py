from credentials import * # This is the file that has the credentials to
                          # connect to the database.
import mysql.connector
import re

#####################################################################
# get_messages
#   Grab all the messages.
#####################################################################
def get_messages(cursor):
    cursor.execute('''
            DESC message_keyword;
        ''')
    messages = cursor.fetchall()

    print(messages)

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