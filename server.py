import cherrypy
import logging

from helpers.config_helper import ConfigHelper
from controllers.ac import Ac

config_helper = ConfigHelper()
logger = logging.getLogger(__name__)

class VortexSmartAc(object):

    config_helper = None
    ac = None

    def __init__(self, config_helper):
        self.config_helper = config_helper
        self.ac = Ac(config_helper)

    @cherrypy.expose
    def index(self):
        return "Vortex Smart AC service. No UI's, only API's"


cherrypy.config.update({
        'server.socket_host': config_helper.server_bind_address,
        'server.socket_port': config_helper.server_port
    })

cherrypy.quickstart(VortexSmartAc(config_helper))