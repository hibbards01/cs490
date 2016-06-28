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
import math
from operator import itemgetter
total = 500

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

    # print(suicidalTotal)
    # print(keywords)

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

    # print(regularTotal)

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

    # print(total)
    deleteKeys = []
    for key, value in suicidal.items():
        if key in regular:
            keywords[key] = value + regular[key]
        else:
            deleteKeys.append(key)

    for key in deleteKeys:
        suicidal.pop(key, None)

    # print(keywords)
    for key, value in keywords.items():
        probKeyword = value / total # P(W)
        probKeywordGivenSuicide = suicidal[key] / suicidalTotal # P(W|S)
        suicidal[key] = probKeywordGivenSuicide / probKeyword # P(S|W)

    sort = sorted(suicidal.items(), key=itemgetter(1), reverse=True)

    maxNum = sort[0][1]
    minNum = sort[len(sort) - 1][1]

    # print(maxNum, " ", minNum)

    for key, value in suicidal.items():
        # print("BEFORE")
        # print(suicidal[key])
        suicidal[key] = (suicidal[key] - minNum) / (maxNum - minNum)
        # print(suicidal[key])
        # print("AFTER")

    print(sorted(suicidal.items(), key=itemgetter(1), reverse=True))
    return suicidal

def getTable():

    arr = []

    global user
    global password
    global host
    global database

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

    try:
        cursor = cnx.cursor()

        suicidal = getSuicide(cursor)
        regular = getRegular(cursor)

        arr = createTable(suicidal, regular)
    finally:
        cnx.close()

    return arr

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