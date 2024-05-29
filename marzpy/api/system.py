from .send_requests import send_request


class System:
    def __init__(self, session) -> None:
        self.session = session

    async def get_system_stats(self):
        """get server stats.

        Returns:
            `~dict`: server stats
        """
        return await send_request(endpoint="system", token=self.session.token, method="get")

    async def get_inbounds(self):
        """get server inbounds.

        Returns:
            `~dict`: server inbounds
        """
        return await send_request(endpoint="inbounds", token=self.session.token, method="get")

    async def get_hosts(self):
        """get server hosts.

        Returns:
            `~dict`: server hosts
        """
        return await send_request(endpoint="hosts", token=self.session.token, method="get")

    async def modify_hosts(self, data: dict):
        """get server hosts.

        Parameters:
            data (``dict``) : new hosts data
        Returns:
            `~dict`: server hosts
        """
        return await send_request(endpoint="hosts", token=self.session.token, method="put", data=data)
