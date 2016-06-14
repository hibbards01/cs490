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
total = 100

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
            SELECT SUM(total) FROM keywords_regular
        ''')

    global regularTotal
    regularTotal = int(cursor.fetchall()[0][0])

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
def createTable(suicidal):
    keywords = {}

    global suicidalTotal, regularTotal

    total = suicidalTotal + regularTotal

    for key, value in suicidal.items():
        keywords[key] = value

    print(total)
    deleteKeys = []
    for key,value in keywords.items():
        probKeyword = value / total # P(W)
        try:
            print("_______BEGIN_______")
            print(suicidal[key], " ", probKeyword, " ", suicidalTotal)
            probKeywordGivenSuicide = suicidal[key] / suicidalTotal # P(W|S)
            print(math.log10(probKeywordGivenSuicide), " ", math.log10(probKeyword))
            suicidal[key] = math.log10(probKeywordGivenSuicide) - math.log10(probKeyword) # P(S|W)
            print(suicidal[key])
            print("____________END___________")
        except:
            deleteKeys.append(key)
            if key in suicidal:
                del suicidal[key]

    for key in deleteKeys:
        keywords.pop(key, None)

    sorted(suicidal.items(), key=itemgetter(1), reverse=True)

    normalize = list(suicidal.values())[0]

    for key, value in suicidal.items():
        suicidal[key] /= normalize

    print(suicidal)

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
        getRegular(cursor)

        createTable(suicidal)
    finally:
        cnx.close()

if __name__ == '__main__':
    main()