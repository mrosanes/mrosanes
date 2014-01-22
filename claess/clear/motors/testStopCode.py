import unittest
import random
import PyTango

#importat per poder utilitzar la macro mv i altres: (maybe)
#import sardana.macroserver.macros (maybe)

# SCRIPT USED TO SEE IF WE CAN REALIZE 50 MOVEMENTS WITHOUT SEEING AN ANORMAL
# STOPCODE: FOR INSTANCE WE DO NOT WANT "SETTLING TIME ERROR"


# Basar-me amb els scripts motorcharacterization (the one from rhoms and the
# one from mrosanes)


# Our limits for positions given by the Clear structure are: 
# Lower limit: 43degrees 
# Higher limit: 76degrees

# Thus, to do safe movements we will move between 50degrees and 73degrees. 
# Moreover, in a paper indicated by Iulian, it seems that 
# angles lower than 55degrees loses too much resolution.


# The user will give as input the name of the motor to be tested.
dummot = PyTango.DeviceProxy("motor/dummotctrl/7") 



# Preguntar com a input quin dels motors volem moure
# pseudomotortotest = braggth ###########a reposar al codi

#positions = [60, 65] ######### sol com a test del test #(basura)

text_file = open("Output.txt", "w")

count = 0

print("Position at the very beginning of the script {0}:\n".format(dummot.Position))

# 5*len(positions) = 5*8 = 48 movements
for i in range(0, 1):
#for i in range(0, 6):

    #positions = [50.0, 54.5, 57.777, 60.569, 64.125, 68.478, 71.333, 72.999]
    positions = [60.0, 58.5]

    for j in range(0, len(positions)): 
        
        count = count+1
        pos = random.choice(positions)
        positions.remove(pos)
        dummot.Position = pos

        motor_on = "ON"
        while (motor_on not in str(dummot.State())): 
            pass
        
        stopcode = "hiho"

        text_file.write("StopCode {0} at pos {1} is: {2}\n".format(count, pos, stopcode))
        print("Position after moving to the new position is {0}:\n".format(dummot.Position))
    
text_file.close()


