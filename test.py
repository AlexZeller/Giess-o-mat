########### This is a temporary test file. Can be overwritten at any point #########

from giessomat import L298n

fan = L298n.L298n(24, 23, 25)

fan.run(50)