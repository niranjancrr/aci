import sys
import os
path = os.getenv('PYTHONPATH')
connections = path + '/aci/connections/'
logging = path + '/aci/logging/'
sys.path.append('connections')
sys.path.append('logging')
from AVE import AVE
#sys.path.append('/auto/AVS1/niranjan/scripts/framework/aci/connections/')
#sys.path.append('/auto/AVS1/niranjan/scripts/framework/aci/logging/')
