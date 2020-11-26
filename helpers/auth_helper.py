import cherrypy
from helpers.config_helper import ConfigHelper


class AuthHelper:

    secret = None

    def __init__(self, config_helper: ConfigHelper):
        self.secret = config_helper.service_secret

    def check_auth(self):
        try:
            print("------")
            print(cherrypy.request.headers)
            bearer_token_parts = cherrypy.request.headers["Authorization"].split(" ")
        except KeyError as e:
            print(e)
            raise cherrypy.HTTPError(
                401,
                'Invalid Authorization header'
            )

        if len(bearer_token_parts) != 2:
            raise cherrypy.HTTPError(
                401,
                'Invalid Authorization header'
            )
        if bearer_token_parts[0].lower() != "bearer":
            raise cherrypy.HTTPError(
                401,
                'Invalid Authorization header'
            )
        if bearer_token_parts[1] != self.secret:
            raise cherrypy.HTTPError(
                403,
                'Forbidden'
            )
