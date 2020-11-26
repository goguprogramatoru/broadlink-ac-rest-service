import cherrypy
from helpers.config_helper import ConfigHelper
from services.ac_service import AcService
from helpers.ac_db import Device
from helpers.auth_helper import AuthHelper


class Ac:

    config_helper: ConfigHelper = None
    ac_service: AcService = None
    auth_helper: AuthHelper = None

    def __init__(self, config_helper):
        self.config_helper = config_helper
        self.ac_service = AcService(config_helper)
        self.auth_helper = AuthHelper(config_helper)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def status(self):
        """
        Get the status of the AC unit
        """
        self.auth_helper.check_auth()
        try:
            device_mac = cherrypy.request.headers["x-device-mac"]
        except KeyError:
            raise cherrypy.HTTPError(
                400,
                'No x-device-mac header'
            )
        device = self.ac_service.devices[device_mac]
        return device.get_ac_status()

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def discover(self):
        """
        Tries to find the available AC units on registered on the network.
        You can do this manually, by checking the connected devices in your router app.
        """

        self.auth_helper.check_auth()

        devices_to_show = []

        devices_discovered = self.ac_service.discover()

        for mac in devices_discovered:
            device: Device = devices_discovered[mac]

            mac = ":".join([mac.upper()[i:i + 2] for i in range(0, len(mac), 2)])

            devices_to_show.append(
                {"mac": mac, "ip": device.host[0], "port": device.host[1]}
            )

        return {"discovered": devices_to_show}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def list(self):
        """
        List the devices that were successfully loaded from the config
        """

        self.auth_helper.check_auth()
        devices_to_show = []

        devices = self.ac_service.devices

        for mac in devices:
            device: Device = devices[mac]
            devices_to_show.append(
                {"mac": mac, "ip": device.host[0], "port": device.host[1]}
            )

        return {"initialized": devices_to_show}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    @ cherrypy.tools.json_in()
    def command(self):
        """
        Send a command to the ac unit.
        """

        self.auth_helper.check_auth()

        try:
            device_mac = cherrypy.request.headers["x-device-mac"]
        except KeyError:
            raise cherrypy.HTTPError(
                400,
                'No x-device-mac header'
            )

        try:
            input_json = cherrypy.request.json
            command = input_json["command"].lower()
            param = input_json["param"].lower()
        except KeyError:
            raise cherrypy.HTTPError(
                400,
                'You should POST a json that contains the following fields: device_mac'
            )

        device = self.ac_service.devices[device_mac]

        if command == "power":
            if param == "on":
                device.switch_on()
            elif param == "off":
                device.switch_off()
            else:
                raise cherrypy.HTTPError(400, 'Unrecognized param. Options: on/off')
        elif command == "temperature":
            try:
                temperature: int = int(param)
            except ValueError:
                raise cherrypy.HTTPError(400, 'The param should be an int (the temperature in celsius)')

            if temperature < 16 or temperature > 32:
                raise cherrypy.HTTPError(400, 'The temperature param should be between 16 and 32')

            device.set_temperature(temperature)
        elif command == "mode":
            available_modes = ["cooling", "dry", "heating", "auto", "fan"]
            if param not in available_modes:
                raise cherrypy.HTTPError(400, 'The param options: '+" ".join(available_modes))
            device.set_mode(param)
        else:
            raise cherrypy.HTTPError(400, 'Unrecognized command. Options: power, temperature, mode')

        return {"success": True}
