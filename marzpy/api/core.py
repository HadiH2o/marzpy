from .send_requests import *


class Core:
    def __init__(self, session) -> None:
        self.session = session

    async def get_xray_core(self):
        """get xray core.

        **Returns:**
            (dict): xray core
        """
        return await send_request(endpoint="core", session=self.session, method="get")

    async def restart_xray_core(self):
        """restart xray core.
        **Returns:**
            (str): success
        """
        await send_request(endpoint="core/restart", session=self.session, method="post")
        return "success"

    async def get_xray_config(self):
        """get xray config.

        **Returns:**
            (dict): xray config
        """
        return await send_request(endpoint="core/config", session=self.session, method="get")

    async def modify_xray_config(self, config: json):
        """edit xray config.

        **Parameters:**
            * `config` (json): json of new config`

        **Returns:**
            (str): success
        """
        await send_request(endpoint="core/config", session=self.session, method="put", data=config)
        return "success"


# ToDo : add possible errors on Core class functions.
