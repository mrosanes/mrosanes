# HOW TO CALL THE SCRIPT:
# python testStopCode.py motors --clear=True --n=1
# Where 'motors' is a file containing a list with pseudomotor, motors and 
# positions.


# SCRIPT USED TO SEE IF WE CAN REALIZE 50 MOVEMENTS WITHOUT SEEING AN ANORMAL
# STOPCODE: FOR INSTANCE WE DO NOT WANT "SETTLING TIME ERROR"  

import unittest
import random
import PyTango
import argparse



parser = argparse.ArgumentParser(description='test a motor StopCode')

parser.add_argument('file', metavar='fname', type=str,
                   help='list with pseudomotor and physical motors composing' + 
			            'it, to be tested: StopCode')   
parser.add_argument('--n','--ntimes', type=int, default=1,
                   help='number of times that each position will be tested')
parser.add_argument('--c','--clear', type=bool, default=False,
                   help='Give True if you want to test CLEAR bragg pseudo')


args = parser.parse_args()




f = open(args.file, 'r')
text_file = open("StopCodes.txt", "w")

# The motor_list shall contain the pseudomotor as first motor in the list and 
# all the physical motors listed after it.

motors = f.readline()
motors_list = motors.split()

pseudomotor_name = motors_list[0]
physical_motors_names = motors_list[1:]

print('\nPseudomotor is: {0}'.format(pseudomotor_name))
text_file.write('\nPseudomotor is: {0}\n'.format(pseudomotor_name))

print('Physical motors are: {0}'.format(physical_motors_names))
text_file.write('Physical motors are: {0}\n'.format(physical_motors_names))

pseudomotor = PyTango.DeviceProxy(pseudomotor_name)


physical_motors = []
for i in range (0, len(physical_motors_names)):
    physicalmot = PyTango.DeviceProxy(physical_motors_names[i])    
    physical_motors.append(physicalmot)



positions = f.readline()
position_str_list = positions.split()
position_list=[]
for i in range (0, len(position_str_list)):
    position_list.append(float(position_str_list[i]))    
   


###########   Limits for CLEAR in bragg Pseudomotor   ###########
########### Indicate --clear=True in the script call  ###########
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

print('Positions to be reach for pseudo are: {0}\n'.format(position_list))
text_file.write('Positions to be reach for pseudo are: {0}\n'.format(position_list))



count = 0

print('\nPosition of pseudo at the beginning of the script is {0}:\n'
                                            .format(pseudomotor.Position))
text_file.write('\nPosition of pseudo at the beginning of the script is {0}:\n'
                                            .format(pseudomotor.Position))

for i in range(0, args.n):

    positions = []

    for i in range(0, len(position_list)):
        positions.append(position_list[i])

    text_file.write('---------\n')
    text_file.write("\nPositions: {0}\n".format(positions))
    print("\nPositions: {0}".format(positions))
    

    for j in range(0, len(positions)): 
                
        count = count+1
        posit = random.choice(positions)
        positions.remove(posit)
        pseudomotor.Position = posit

        motor_on = "ON"
        while (motor_on not in str(pseudomotor.State())): 
            pass
 

        for u in range(0, len(physical_motors)):
            physical_motors[u].read_attribute("Status")    

            try:            
                stopcode = physical_motors[u].read_attribute("StatusStopCode").value
            except:
                stopcode = "StopCode does NOT exist for this motor"
        
            text_file.write('StopCode at pseudoposition {0} for physicalmotor {1} is: {2}\n'
            .format(pseudomotor.Position, physical_motors[u].alias(), stopcode))

            print('StopCode at pseudoposition {0} for physicalmotor {1} is: {2}'
                          .format(posit, physical_motors[u].alias(), stopcode))
    
        text_file.write('\n')


f.close()
text_file.close()
print('\n')


