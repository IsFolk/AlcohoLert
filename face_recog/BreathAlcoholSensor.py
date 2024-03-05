import spidev
import time

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000
 
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


#print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
#print('-' * 57)

def get_concentration():
    
    # Main program loop.
    while True:
        # Read all the ADC channel values in a list.
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            data = readadc(i)
            values[i] = round (data * (3.3/1023.0), 2)
        # Print the ADC values.
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
        
        #print("Alcohol Concentration:",(values[0]-1.3)/2.778))  #
        # Pause for half a second.
        time.sleep(0.5)
        
        return values[0]
        
#get_concentration()
