#!/usr/bin/python
######################################################################
# Program:
#   neural_network.py
# Author:
#   Samuel Hibbard
# Summary:
#   This will grab from the databases and see if we can predict a high
#       and low risk suicide person.
#
#   NOTE: In order to be able to run this you must install
#   mysql.connector from ORACLE.
######################################################################

import mysql.connector
import sys
from credentials import * # This is the file that has the credentials to
                          # connect to the database.

def main(args):
    # Grab everything
    global user
    global password
    global host
    global database

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

    try:
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT * FROM user;
        """)
        result = cursor.fetchall()
        print(result)
    finally:
        cnx.close()

if __name__ == '__main__':
    main(sys.argv)