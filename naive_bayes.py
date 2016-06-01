#!/usr/bin/python
###########################################################################
# Program:
#   decision_tree.py
# Author:
#   Samuel Hibbard
# Summary:
#   This will grab the data from the database and train the decision tree
#       from it.
###########################################################################

from credentials import * # This is the file that has the credentials to
                          # connect to the database.
import mysql.connector

#####################################################################
# getSuicide
#   Grab all the numbers for the keywords of the suicidal people.
#####################################################################
def getSuicide(cursor):
    cursor.execute('''
            SELECT * FROM keywords_suicidal WHERE total > 100 ORDER BY total DESC
        ''')

    array = dict(cursor.fetchall())
    keywords = { key.decode("utf-8"):value for key,value in array.items() }

    cursor.execute('''
            SELECT COUNT(*) FROM keywords_suicidal WHERE total > 100 ORDER BY total DESC
        ''')

    keywords['totalKeywords'] = int(cursor.fetchall()[0][0])

    cursor.execute('''
            SELECT SUM(total) FROM keywords_suicidal WHERE total > 100
        ''')

    keywords['totalUseOfKeywords'] = int(cursor.fetchall()[0][0])

    return keywords

#####################################################################
# getRegular
#   Grab all the people that are not suicidal.
#####################################################################
def getRegular(cursor):
    cursor.execute('''
            SELECT * FROM keywords_regular WHERE total > 100 ORDER BY total DESC
        ''')

    array = dict(cursor.fetchall())
    keywords = { key.decode("utf-8"):value for key,value in array.items() }

    cursor.execute('''
            SELECT COUNT(*) FROM keywords_regular WHERE total > 100 ORDER BY total DESC
        ''')

    keywords['totalKeywords'] = int(cursor.fetchall()[0][0])

    cursor.execute('''
            SELECT SUM(total) FROM keywords_regular WHERE total > 100
        ''')

    keywords['totalUseOfKeywords'] = int(cursor.fetchall()[0][0])

    return keywords

#####################################################################
# createTable
#   This will create the probability tables.
#####################################################################
def createTable(suicidal, regular):
    # Loop through the keywords and add the probabilities
    for key, value in suicidal.items():
        pass

#####################################################################
# main
#   Driver program.
#####################################################################
def main():
    global user
    global password
    global host
    global database

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

    try:
        cursor = cnx.cursor()

        suicidal = getSuicide(cursor)
        regular = getRegular(cursor)

        createTable(suicidal, regular)
    finally:
        cnx.close()

if __name__ == '__main__':
    main()