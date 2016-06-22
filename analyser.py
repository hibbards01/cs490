import sys
import naive_bayes
from credentials import * # This is the file that has the credentials to
                          # connect to the database.
import mysql.connector
from operator import itemgetter

def analyseUser(id, cursor):

    cursor.execute('''
            select k.text as keyword, count(0) as total
            from message m, keyword k, message_keyword mk
            where m.user_id = %s
            and m.id = mk.message_id
            and k.id = mk.keyword_id
            group by k.text
            order by count(0) desc
        ''', (id,))

    array = dict(cursor.fetchall())
    total = sum(array.values())

    wordsSum = 0

    for key, value in array.items():
        word = key.decode("utf-8")
        try:
            # print(table[word])
            wordsSum += table[word] * value
        except:
            total -= value
        # print(word, value)
    if not total:
        return 0
    return wordsSum / total



#####################################################################
# main
#   Driver program.
#####################################################################
def main():
    global user
    global password
    global host
    global database
    global table

    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

    try:
        cursor = cnx.cursor()

        table = naive_bayes.getTable()
        # print(table)

        users = {}
        for i in range(int(sys.argv[1]), int(sys.argv[2])):
            users[i] = analyseUser(i, cursor)
        sort = sorted(users.items(), key=itemgetter(1), reverse=True)
        print(sort)
    finally:
        cnx.close()
    

if __name__ == '__main__':
    main()