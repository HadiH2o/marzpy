from typing import Union, List

from .send_requests import *


class Admin:
    def __init__(self, username: str, is_sudo: bool, password: str = None, telegram_id: int = None, discord_webhook: str = None, session=None):
        self.username = username
        self.is_sudo = is_sudo
        self.password = password
        self.telegram_id = telegram_id
        self.discord_webhook = discord_webhook
        self.methods = AdminMethods(session)

    async def modify(self, admin: "Admin") -> "Admin":
        return await self.methods.modify_admin(self.username, admin)

    async def delete(self) -> str:
        return await self.methods.delete_admin(self.username)


class AdminMethods:
    def __init__(self, session):
        self.session = session

    async def get_token(self, panel_address: str, username: str, password: str) -> Union[None, dict]:
        """login for Authorization token

        **Parameters:**
            * `panel_address` (str): panel address
            * `username` (str): username of admin
            * `password` (str):  password of admin

        **Returns:**
            (dict): Authorization token

        """
        try:
            async with aiohttp.request(
                    "post",
                    url=f"{panel_address}/api/admin/token",
                    data={"username": username, "password": password},
            ) as response:
                result = await response.json()
                result["panel_address"] = panel_address
                return result

        except aiohttp.exceptions.RequestException as ex:
            print(f"Request Exception: {ex}")
            return None

        except json.JSONDecodeError as ex:
            print(f"JSON Decode Error: {ex}")
            return None

    async def get_current_admin(self) -> Admin:
        """get current admin who has logged in.

        **Returns:**
            (Admin): information of current admin
        """
        response = await send_request(endpoint="admin", token=self.session.token, method="get")
        return Admin(**response, session=self.session)

    async def create_admin(self, admin: Admin) -> Admin:
        """add new admin.

        **Parameters:**
            * `admin` (Admin) : information of new admin

        **Returns:**
            (Admin): information of new admin

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `AdminAlreadyExists` : admin already exists
            * `AdminInvalidEntity` : admin information is invalid
        """
        response = await send_request(endpoint="admin", token=self.session.token, method="post", data=admin.__dict__)
        return Admin(**response, session=self.session)

    async def modify_admin(self, username: str, admin: Admin) -> Admin:
        """change exist admins password.

        *you cant modify sudo admins password*

        **Parameters:**
            * `username` (str) : username of admin
            * `admin` (Admin) : information of new admin

        **Returns:**
            (Admin): information of new admin

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `AdminNotFound` : admin not found
            * `AdminInvalidEntity` : admin information is invalid
        """
        admin_dict = admin.__dict__
        admin_dict.pop('username')
        response = await send_request(endpoint=f"admin/{username}", token=self.session.token, method="put", data=admin_dict)
        return Admin(**response, session=self.session)

    async def delete_admin(self, username: str) -> str:
        """delete admin.

        **Parameters:**
            * `username` (str): username of admin

        **Returns:**
            (str): success

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `AdminNotFound` : admin not found
            * `AdminInvalidEntity` : admin information is invalid
        """
        await send_request(endpoint=f"admin/{username}", token=self.session.token, method="delete")
        return "success"

    async def get_admins(self) -> List[Admin]:
        """get all admins.

        **Returns:**
            (List[Admin]): list of all admins

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `AdminInvalidEntity` : admin information is invalid
        """
        response = await send_request(endpoint=f"admins", token=self.session.token, method="get")
        result = [Admin(**admin, session=self.session) for admin in response]
        return result
