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

import math
import mysql.connector
from fann2 import libfann as nn
import sys
from credentials import * # This is the file that has the credentials to
                          # connect to the database.

#####################################################################
# train_network
#   This will train the network based off the file given.
#####################################################################
def train_network(file):
    print('\nTraining Network from this file:', file, '\n')

    # Setup all the variables
    connection_rate = 1
    learning_rate = 0.7
    num_input = 2
    num_hidden = 4
    num_output = 1

    desired_error = 0.0001
    max_iterations = 100000
    iterations_between_reports = 1000

    ann = nn.neural_net()
    ann.create_sparse_array(connection_rate, (num_input, num_hidden, num_output))
    ann.set_learning_rate(learning_rate)
    ann.set_activation_function_output(nn.SIGMOID_SYMMETRIC_STEPWISE)

    ann.train_on_file(file, max_iterations, iterations_between_reports, desired_error)

    ann.save(file.replace('.data', '.net'))

#####################################################################
# test_network
#   Test the network.
#####################################################################
def test_network(file_name):
    # Grab testing file from the user
    test_file = input('\nWhat file do you want to test on?: ')

    # Now read from the file
    file = open(test_file, 'r')

    # Loop through the file line by line and grab the input and outputs
    inputs = []
    outputs = []
    num = 0
    for line in file:
        array = line.split(',')
        nums = [int(i)  for i in array]
        if num % 2 == 0:
            inputs.append(nums)
        else:
            outputs.append(nums)

        num += 1

    ann = nn.neural_net()
    ann.create_from_file(file_name)

    # Now test the network
    correct = 0
    for i, inpt in enumerate(inputs):
        answer = ann.run(inpt)
        answer = math.ceil(outputs[i][0] - answer[0])

        if answer == outputs[i][0]:
            correct += 1

    print('\nAccuracy is ', (correct / len(outputs)) * 100, '%\n')


#####################################################################
# main
#   Driver function.
#####################################################################
def main(args):
    # Grab the args
    inputs = {'-help': None, '-train': None, '-test': None}
    error = None

    for i, input in enumerate(args):
        if input in inputs:
            if input == '-help':
                inputs[input] = True
            elif (i + 1) < len(args):
                if input == '-train' or input == '-test':
                    inputs[input] = args[i + 1]
            else:
                error = '\nError: No value given for argument %s.\nType -help for help.\n' % input

    if error is not None:
        print(error)
    elif inputs['-help'] is not None:
        print('\nCommand line arguments for decision_tree.py:\n\n'
            '    py decision_tree.py [options] [value]\n\n'
            '    Options:\n'
            '\t-train,   Give a file that the network will train itself on. It will output\n'
            '\t          a network file once it is finished. That is what you will use to\n'
            '\t          test it on the testing data.\n'
            '\t-test,    Specify the network file that you want to test with. It will then\n'
            '\t          ask you for the testing file data.\n'
            '\t-help,    Show this.\n')
    elif inputs['-train'] is not None or inputs['-test'] is not None:
        if inputs['-train']:
            train_network(inputs['-train'])
        else:
            test_network(inputs['-test'])
    else:
        print('\nNo arguments given type -help for help.\n')

    # global user
    # global password
    # global host
    # global database

    # cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)

    # try:
    #     cursor = cnx.cursor()
    #     cursor.execute("""
    #         SHOW tables;
    #     """)
    #     result = cursor.fetchall()
    #     print(result)
    # finally:
    #     cnx.close()

    # print(ann.run([1, 0]))
    # print(ann.run([0, 1]))
    # print(ann.run([1, 1]))
    # print(ann.run([0, 0]))


if __name__ == '__main__':
    main(sys.argv)