import time
import sys
import Adafruit_MPR121.MPR121 as MPR121

# Create MPR121 instance.
def initialize():
    print "starting..."

cap = MPR121.MPR121() 
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)  

cap.set_Thresholds(255,255)

def detect():
   
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.

    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            #touched.append(i)
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
            #touched.remove(i)
    # Update last state and wait a short period before repeating.
    last_touched = cap.touched
    time.sleep(0.1) 

def loopDetect():
    last_touched = cap.touched()
    while True:
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))
        # Update last state and wait a short period before repeating.
        last_touched = current_touched
        time.sleep(0.1)
 
def main():
    initialize()
    '''while True:
        detect()'''
    loopDetect()
if __name__ == '__main__':
    main()

