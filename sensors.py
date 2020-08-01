import logging
from giessomat import Database

# Set up logging
logging.basicConfig(filename='giessomat.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
log = logging.getLogger(__name__)

log.info('Starting forced senor reading...')

# Read sensor values and write to database
try:
    db = Database.Database('/home/pi/Giess-o-mat/giessomat_db.db')
    db.sensordata2database()
    db.log2database('Sensors', 'success', 'Wrote sensor values to database')
except:
    log.critical('Failed to read sensor values/write to database')
    db.log2database('Sensors', 'error', 'Error writing sensor values to database')

log.info('Finished!')
