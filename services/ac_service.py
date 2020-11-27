import logging
import time
from helpers.config_helper import ConfigHelper
from helpers.ac_db import Tools as AcDbTools


class AcService:

    config_helper: ConfigHelper = None
    logger = logging.getLogger(__name__)

    devices = {}

    def __init__(self, config_helper):
        self.config_helper = config_helper
        self.devices = self.load_devices_from_config()

    def discover(self):
        discovered_devices = AcDbTools().discover(timeout=5)
        devices = {}

        if discovered_devices is None:
            error_msg = "No Devices Found, make sure you on the same network segment"
            self.logger.debug(error_msg)

            # empty
            return devices

        # Make sure correct device id
        for device in discovered_devices:
            if device.devtype == 0x4E2a:
                devices[device.status['macaddress']] = device

        return devices

    def load_devices_from_config(self):

        device_list = self.config_helper.yaml_config["devices"]

        device_objects = {}
        if device_list == [] or device_list is None:
            self.logger.error("Empty list of devices specified in the config file")
            return

        retry = True
        while retry == True:
            for device in device_list:
                try:
                    device_objects[device['mac']] = AcDbTools().generate_device(
                        devtype=0x4E2a,
                        host=(device['ip'], device['port']),
                        mac=bytearray.fromhex(device['mac'].replace(":", "")),
                        name=device['name']
                    )
                    retry = False
                except Exception:
                    time.sleep(1)
                    self.logger.warn("Timeout, trying again in 1 sec")
                    retry = True

        return device_objects
