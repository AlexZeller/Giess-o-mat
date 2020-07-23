import sys
from time import sleep
from giessomat import MCP3008, Relais


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print('This utility will check all connected components of the Giess-o-mat')
print(bcolors.WARNING + 'It will turn on and off all Relais channels' + bcolors.ENDC)
input = raw_input('Do you want to proceed (y/n)?: ')

if input == 'n':
    print('Exiting utility')
    sys.exit()
elif input == 'y':

    print(bcolors.HEADER + 'Checking all connected components...' + bcolors.ENDC)
    sleep(1)
    print('Checking MCP3008 Channels...')
    sleep(1)
    ADC = MCP3008.MCP3008()
    channel_readings = [None]*8
    for i in range(0, 8):
        channel_readings[i] = ADC.read_channel(i)
        print('Channel' + str(i) + ': ' + str(channel_readings[i]))
        sleep(1)
    if not all(readings == 0 for readings in channel_readings):
        print(bcolors.OKGREEN +
              '[MCP3008 OKAY] Not all channels are 0, interpreting as successfully connected' + bcolors.ENDC)
    else:
        print(bcolors.WARNING +
              '[MCP3008 WARNING] All channels are 0, interpreting as not successfully connected' + bcolors.ENDC)
    print('Checking Relais')
    print('You should hear an audible click each time the relais is switching states')
    sleep(3)
    relais_1 = Relais.Relais(23)
    relais_2 = Relais.Relais(24)
    relais_3 = Relais.Relais(24)
    relais_4 = Relais.Relais(16)
    print('Switching Relais channel 1 on...')
    relais_1.on()
    sleep(2)
    print('Switching Relais channel 1 off...')
    relais_1.off()
    sleep(2)
    print('Switching Relais channel 2 on...')
    relais_2.on()
    sleep(2)
    print('Switching Relais channel 2 off...')
    relais_2.off()
    sleep(2)
    print('Switching Relais channel 3 on...')
    relais_3.on()
    sleep(2)
    print('Switching Relais channel 3 off...')
    relais_3.off()
    sleep(2)
    print('Switching Relais channel 4 on...')
    relais_4.on()
    sleep(2)
    print('Switching Relais channel 4 off...')
    relais_4.off()
    sleep(2)

    print(bcolors.OKBLUE + 'Finished Check.' + bcolors.ENDC)
