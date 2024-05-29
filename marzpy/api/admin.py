from .send_requests import *


class Admin:
    def __init__(self, username: str, is_sudo: bool, password: str, telegram_id: int = None, discord_webhook: str = None, ):
        self.username = username
        self.is_sudo = is_sudo
        self.password = password
        self.telegram_id = telegram_id
        self.discord_webhook = discord_webhook


class AdminMethods:
    def __init__(self, session):
        self.session = session

    async def get_token(self, panel_address: str, username: str, password: str):
        """login for Authorization token

        Returns: `~dict`: Authorization token
        """
        try:
            async with aiohttp.request(
                    "post",
                    url=f"{panel_address}/api/admin/token",
                    data={"username": username, "password": password},
            ) as response:
                # response.raise_for_status()  # Raise an exception for non-200 status codes
                result = await response.json()
                result["panel_address"] = panel_address
                return result

        except aiohttp.exceptions.RequestException as ex:
            print(f"Request Exception: {ex}")
            return None

        except json.JSONDecodeError as ex:
            print(f"JSON Decode Error: {ex}")
            return None

    async def get_current_admin(self):
        """get current admin who has logged in.

        Returns:
        `~dict`: {"username": "str" , "is_sudo": true}
        """
        return await send_request(endpoint="admin", token=self.session.token, method="get")

    async def create_admin(self, admin: Admin):
        """add new admin.

        Parameters:
            admin (``Admin``) : information of new admin

        Returns:
        `~dict`: username && is_sudo
        """
        await send_request(endpoint="admin", token=self.session.token, method="post", data=admin.__dict__)
        return "success"

    async def modify_admin(self, username: str, admin: Admin):
        """change exist admins password.

        *you cant modify sudo admins password*

        Parameters:
            username (``str``) : username of admin
            admin (``Admin``) : information of new admin

        Returns:
        `~dict`: username && is_sudo
        """
        admin_dict = admin.__dict__
        admin_dict.pop('username')
        await send_request(
            endpoint=f"admin/{username}",
            token=self.session.token,
            method="put",
            data=admin_dict,
        )
        return "success"

    async def delete_admin(self, username: str):
        """delete admin.

        Parameters:
            username (``str``) : username of admin

        Returns:
        `~str`: success
        """
        await send_request(endpoint=f"admin/{username}", token=self.session.token, method="delete")
        return "success"

    async def get_all_admins(self):
        """get all admins.

        Returns:
        `~list`: [{username && is_sudo}]
        """
        return await send_request(endpoint=f"admins", token=self.session.token, method="get")
