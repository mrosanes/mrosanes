# HOW TO CALL THE SCRIPT:
# python testStopCode.py 58 62 63.36 --n=3 --c=True --mot=motorname

import unittest
import random
import PyTango
import argparse


# SCRIPT USED TO SEE IF WE CAN REALIZE 50 MOVEMENTS WITHOUT SEEING AN ANORMAL
# STOPCODE: FOR INSTANCE WE DO NOT WANT "SETTLING TIME ERROR"    


parser = argparse.ArgumentParser(description='test a motor StopCode')

parser.add_argument('pos', metavar='pos', type=float, nargs='+', 
                   help='positions as list of floats')                   
parser.add_argument('--mot', '--motor', type=str, default='motor/dummotctrl/7',
                   help='pseudomotor or motor to be studied')
parser.add_argument('--n','--ntimes', type=int, default=1,
                   help='number of times that each position will be tested')
parser.add_argument('--c','--clear', type=bool, default=False,
                   help='Give True if you want to test CLEAR bragg pseudo')

args = parser.parse_args()




position_list = args.pos


########### Limits for CLEAR in bragg Pseudomotor ###########
#Clear bragg pseudo must be limited (for the moment) to 50degrees and 73degrees.

low_lim = 50
high_lim = 73

if (args.c == True):
    for i in range (0, len(position_list)):
        if (position_list[i]>= high_lim):
            position_list[i] = high_lim
        elif (position_list[i]<= low_lim):
            position_list[i] = low_lim
        else: 
            position_list[i] = position_list[i]

##############################################################



print(position_list)

motor = PyTango.DeviceProxy(args.mot)

text_file = open("StopCodes.txt", "w")
count = 0

print("\nPosition at the beginning of the script is {0}:\n"
                                            .format(motor.Position))


for i in range(0, args.n):

    positions = []

    for i in range(0, len(position_list)):
        positions.append(position_list[i])

    print("\nPositions: {0}".format(positions))

    for j in range(0, len(positions)): 
        
        count = count+1
        posit = random.choice(positions)
        positions.remove(posit)
        motor.Position = posit

        motor_on = "ON"
        while (motor_on not in str(motor.State())): 
            pass
 
        motor.read_attribute("Status")
        #stopcode = motor.read_attribute("StatusStopCode").value
        stopcode = "hiho"


        text_file.write("StopCode {0} at position {1} is: {2}\n"
                                        .format(count, posit, stopcode))

        print("StopCode {0} at position {1} is: {2}"
                                        .format(count, posit, stopcode))
    


text_file.close()
print('\n')


