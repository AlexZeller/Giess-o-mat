from giessomat import MCP3008

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.HEADER + 'Checking all connected components...'+ bcolors.ENDC)

print('Checking MCP3008 Channels...')
ADC = MCP3008.MCP3008()
channel_readings = [None]*8
for i in range (0,8):
    channel_readings[i] = ADC.read_channel(i)
    print('Channel' + str(i) +': ' + str(channel_readings[i]))
if not all(readings == 0 for readings in channel_readings):
    print(bcolors.OKGREEN + '[MCP3008 OKAY] Not all channels are 0, interpreting as successfully connected'+ bcolors.ENDC)
else:
    print(bcolors.WARNING + '[MCP3008 WARNING] All channels are 0, interpreting as not successfully connected'+ bcolors.ENDC)

print(bcolors.OKBLUE + 'Finished Check.'+ bcolors.ENDC)   