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
from operator import itemgetter
total = 100
suicideProb = 13 / 100000
regularProb = 1 - suicideProb

suicidalTotal = 0
regularTotal = 0

#####################################################################
# getSuicide
#   Grab all the numbers for the keywords of the suicidal people.
#####################################################################
def getSuicide(cursor):
    cursor.execute('''
            SELECT * FROM keywords_suicidal WHERE total > %s ORDER BY total DESC
        ''', (total,))

    array = dict(cursor.fetchall())
    keywords = { key.decode("utf-8"):value for key,value in array.items() }

    cursor.execute('''
            SELECT SUM(total) FROM keywords_suicidal
        ''')

    global suicidalTotal
    suicidalTotal = int(cursor.fetchall()[0][0])

    return keywords

#####################################################################
# getRegular
#   Grab all the people that are not suicidal.
#####################################################################
def getRegular(cursor):
    cursor.execute('''
            SELECT * FROM keywords_regular WHERE total > %s ORDER BY total DESC
        ''', (total,))

    array = dict(cursor.fetchall())
    keywords = { key.decode("utf-8"):value for key,value in array.items() }

    cursor.execute('''
            SELECT SUM(total) FROM keywords_regular
        ''')

    global regularTotal
    regularTotal = int(cursor.fetchall()[0][0])

    return keywords

#####################################################################
# getMax
#####################################################################
def getMax(d):
    v = list(d.values())
    k = list(d.keys())

    return k[v.index(max(v))]

#####################################################################
# createTable
#   This will create the probability tables.
#####################################################################
def createTable(suicidal, regular):
    keywords = {}

    global suicidalTotal, regularTotal

    total = suicidalTotal + regularTotal

    for key, value in suicidal.items():
        keywords[key] = value

    for key, value in regular.items():
        if key not in keywords:
            keywords[key] = value
        else:
            keywords[key] += value

    deleteKeys = []
    for key,value in keywords.items():
        probKeyword = value / total # P(W)
        try:
            probKeywordGivenSuicide = suicidal[key] / suicidalTotal # P(W|S)

            suicidal[key] = probKeywordGivenSuicide * suicideProb / probKeyword # P(S|W)
        except:
            deleteKeys.append(key)
            if key in suicidal:
                del suicidal[key]
            if key in regular:
                del regular[key]

        try:
            probKeywordGivenRegular = regular[key] / regularTotal

            # regular[key] = probKeywordGivenRegular * regularProb / probKeyword
        except:
            deleteKeys.append(key)
            if key in suicidal:
                del suicidal[key]
            if key in regular:
                del regular[key]

    for key in deleteKeys:
        keywords.pop(key, None)

    print(sorted(suicidal.items(), key=itemgetter(1), reverse=True))
    # print(sorted(regular.items(), key=itemgetter(1), reverse=True))


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