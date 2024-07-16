import datetime

import aiohttp

from marzpy.api.exceptions import IncorrectCredentials


class Session:
    def __init__(self, username: str, password: str, panel_address: str):
        self.token = None
        self.expire = None
        self.username = username
        self.password = password
        self.panel_address = panel_address

    async def start(self):
        """login for Authorization token

        Returns: `~dict`: Authorization token
        """
        async with aiohttp.request(
                "post",
                url=f"{self.panel_address}/api/admin/token",
                data={"username": self.username, "password": self.password},
        ) as response:
            result = await response.json()
            if result.get('detail') == 'Incorrect username or password':
                raise IncorrectCredentials('Incorrect username or password')

            else:
                result["panel_address"] = self.panel_address
                self.token = result
                self.expire = datetime.datetime.now() + datetime.timedelta(hours=23)
                return result
