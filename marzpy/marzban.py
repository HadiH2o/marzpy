import aiohttp

from .api import Methods


class Session:
    def __init__(self, username: str, password: str, panel_address: str):
        self.token = None
        self.username = username
        self.password = password
        self.panel_address = panel_address

    async def start_session(self):
        """login for Authorization token

        Returns: `~dict`: Authorization token
        """
        async with aiohttp.request(
                "post",
                url=f"{self.panel_address}/api/admin/token",
                data={"username": self.username, "password": self.password},
        ) as response:
            result = await response.json()
            result["panel_address"] = self.panel_address
            self.token = result
            return result


class Marzban(Methods):
    def __init__(self, session: Session) -> None:
        if isinstance(session.token, dict):
            super().__init__(session)
        else:
            raise "Session Is Not Started Yet"
