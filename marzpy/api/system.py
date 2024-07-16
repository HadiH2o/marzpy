from .send_requests import send_request


class System:
    def __init__(self, session) -> None:
        self.session = session

    async def get_system_stats(self) -> dict:
        """get server stats.

        **Returns:**
            (dict) : server stats
        """
        return await send_request(endpoint="system", session=self.session, method="get")

    async def get_inbounds(self) -> dict:
        """get server inbounds.

        **Returns:**
            (dict) : server inbounds
        """
        return await send_request(endpoint="inbounds", session=self.session, method="get")

    async def get_hosts(self) -> dict:
        """get server hosts.

        **Returns:**
            (dict) : server hosts
        """
        return await send_request(endpoint="hosts", session=self.session, method="get")

    async def modify_hosts(self, data: dict) -> dict:
        """get server hosts.
        **Parameters:**
            * `data` (dict) : new hosts data

        **Returns:**
            (dict) : server hosts
        """
        return await send_request(endpoint="hosts", session=self.session, method="put", data=data)


# ToDo : add possible errors on System class functions.
