from typing import List, Union

from .admin import Admin
from .send_requests import *


async def delete_if_exist(dic, keys: list):
    for key in keys:
        if key in dic:
            del dic[key]
    return dic


class SortEnums:
    asc_username = 'username'
    desc_username = '-username'
    asc_expire = 'expire'
    desc_expire = '-expire'
    asc_created = 'created_at'
    desc_created = '-created_at'
    asc_data_limit = 'data_limit'
    desc_data_limit = '-data_limit'
    asc_used_traffic = 'used_traffic'
    desc_used_traffic = '-used_traffic'


class User:
    def __init__(
            self,
            username: str,
            proxies: dict,
            inbounds: dict,
            data_limit: float,
            data_limit_reset_strategy: str = "no_reset",
            status="",
            expire: float = 0,
            used_traffic=0,
            lifetime_used_traffic=0,
            created_at="",
            links=[],
            subscription_url="",
            excluded_inbounds={},
            note="",
            on_hold_timeout=0,
            on_hold_expire_duration=0,
            sub_updated_at=0,
            online_at=0,
            sub_last_user_agent: str = "",
            auto_delete_in_days: int = None,
            admin: dict = None,
            methods=None
    ):
        self.username = username
        self.proxies = proxies
        self.inbounds = inbounds
        self.expire = expire
        self.data_limit = data_limit
        self.data_limit_reset_strategy = data_limit_reset_strategy
        self.status = status
        self.used_traffic = used_traffic
        self.lifetime_used_traffic = lifetime_used_traffic
        self.created_at = created_at
        self.links = links
        self.subscription_url = subscription_url
        self.excluded_inbounds = excluded_inbounds
        self.note = note
        self.on_hold_timeout = on_hold_timeout
        self.on_hold_expire_duration = on_hold_expire_duration
        self.sub_last_user_agent = sub_last_user_agent
        self.online_at = online_at
        self.sub_updated_at = sub_updated_at
        self.auto_delete_in_days = auto_delete_in_days
        self.admin = Admin(**admin) if admin else None
        self.methods = methods

    async def modify(self, user: "User") -> "User":
        return await self.methods.modify_user(self.username, user)

    async def delete(self) -> str:
        return await self.methods.delete_user(self.username)

    async def reset_traffic(self) -> str:
        return await self.methods.reset_user_traffic(self.username)

    async def revoke_sub(self):
        return await self.methods.revoke_sub(self.username)

    async def get_usage(self):
        return await self.methods.get_user_usage(self.username)


class UserMethods:
    def __init__(self, session):
        self.session = session

    async def add_user(self, user: User) -> User:
        """add new user.

        **Parameters:**
            * `user` (User) : User Object

        **Returns:**
            (User): new user information

        **Raises**:
            * `UserInvalidEntity`: if user information is invalid
            * `UserConflict`: if user already exists
        """
        user.status = "active"

        if user.on_hold_expire_duration:
            user.status = "on_hold"

        request = await send_request(endpoint="user", session=self.session, method="post", data=user.__dict__)
        return User(**request, methods=UserMethods(self.session))

    async def get_user(self, user_username: str) -> User:
        """get exist user information by username.

        **Parameters:**
            * `user_username` (str) : username of user

        **Returns:**
            (User): information of user

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserNotFound`: if user not found
        """
        request = await send_request(f"user/{user_username}", session=self.session, method="get")
        return User(**request, methods=UserMethods(self.session))

    async def modify_user(self, user_username: str, user: object) -> User:
        """edit exist user by username.

        **Parameters:**
            * `user_username` (str) : username of user
            * `user` (User) : User Object

        **Returns:**
            (User): information of edited user

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserInvalidEntity`: if user information is invalid
        """
        request = await send_request(f"user/{user_username}", self.session.token, "put", user.__dict__)
        return User(**request, methods=UserMethods(self.session))

    async def delete_user(self, user_username: str) -> str:
        """delete exist user by username.

        **Parameters:**
            `user_username` (str) : username of user

        **Returns:**
            (str): success

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserNotFound`: if user not found
            * `UserInvalidEntity`: if user information is invalid
        """
        await send_request(f"user/{user_username}", self.session.token, "delete")
        return "success"

    async def reset_user_traffic(self, user_username: str) -> str:
        """reset exist user traffic by username.

        **Parameters:**
            * `user_username` (str) : username of user

        **Returns:**
            (str): success

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserNotFound`: if user not found
            * `UserConflict`: if user already exists
            * `UserInvalidEntity`: if user information is invalid
        """
        await send_request(f"user/{user_username}/reset", self.session.token, "post")
        return "success"

    async def revoke_sub(self, user_username: str) -> User:
        """Revoke users subscription (Subscription link and proxies) traffic by username.

        **Parameters:**
            `user_username` (str) : username of user

        **Returns:**
            (User): information of revoked user

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserNotFound`: if user not found
            * `UserInvalidEntity`: if user information is invalid
        """
        request = await send_request(f"user/{user_username}/revoke_sub", self.session.token, "post")
        return User(**request, methods=UserMethods(self.session))

    async def get_users(self, offset: int = None, limit: int = None, usernames: List[str] = None, status=None, sort: str = None) -> List[User]:
        """get all users list.

        **Parameters:**
            * `offset` (int) : offset
            * `limit` (int) : limit
            * `usernames` (str) : list of usernames
            * `status` (str) : status
            * `sort` (str) : sort (SortEnums)
        **Returns:**
            (List[User]): list of users

        **Raises**:
            * `UserInvalidEntity`: if user information is invalid
        """
        endpoint = "users"
        if offset:
            endpoint += f"?offset={offset}"

        if limit:
            if "?" in endpoint:
                endpoint += f"&limit={limit}"
            else:
                endpoint += f"?limit={limit}"

        if usernames:
            for username in usernames:
                if "?" in endpoint:
                    endpoint += f"&username={username}"
                else:
                    endpoint += f"?username={username}"

        if status:
            if "?" in endpoint:
                endpoint += f"&status={status}"
            else:
                endpoint += f"?status={status}"

        if sort:
            if "?" in endpoint:
                endpoint += f"&sort={sort}"
            else:
                endpoint += f"?sort={sort}"

        request = await send_request(endpoint, self.session.token, "get")
        user_list = [User(**user, methods=UserMethods(self.session)) for user in request["users"]]
        return user_list

    async def reset_all_users_traffic(self):
        """reset all users traffic.

        **Returns:**
            (str): success

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
        """
        await send_request("users/reset", self.session.token, "post")
        return "success"

    async def get_user_usage(self, user_username: str):
        """get user usage by username.

        **Parameters:**
            * `user_username` (str) : username of user

        **Returns:**
            (dict): dict of user usage

        **Raises**:
            * `NotAuthorized` : you are not authorized to do this
            * `UserNotFound`: if user not found
            * `UserInvalidEntity`: if user information is invalid
        """
        return (await send_request(f"user/{user_username}/usage", self.session.token, "get"))["usages"]

    async def get_expired_users(self, expired_before: Union[str, float] = None, expired_after: Union[str, float] = None) -> List[str]:
        """get expired users list.

        **Parameters:**
            * `expired_before` (Union[str, float]) : expired_before specific time (timestamp or isoformat)
            * `expired_after` (Union[str, float]) : expired_after specific time (timestamp or isoformat)

        **Returns:**
            (List[str]) : list of expired usernames

        **Raises**:
            * `UserInvalidEntity`: if time entity is invalid
        """

        endpoint = "users/expired"

        if expired_before:
            endpoint += f"?expired_before={expired_before}"

        if expired_after:
            if "?" in endpoint:
                endpoint += f"&expired_after={expired_after}"
            else:
                endpoint += f"?expired_after={expired_after}"

        return await send_request(endpoint, self.session.token, "get")

    async def delete_expired_users(self, expired_before: Union[str, float] = None, expired_after: Union[str, float] = None) -> List[str]:
        """delete expired users list.

        **Parameters:**
            * `expired_before` (Union[str, float]) : expired_before specific time (timestamp or isoformat)
            * `expired_after` (Union[str, float]) : expired_after specific time (timestamp or isoformat)

        **Returns:**
            (List[str]) : list of expired usernames

        **Raises**:
            * `UserInvalidEntity`: if time entity is invalid
        """

        endpoint = "users/expired"

        if expired_before:
            endpoint += f"?expired_before={expired_before}"

        if expired_after:
            if "?" in endpoint:
                endpoint += f"&expired_after={expired_after}"
            else:
                endpoint += f"?expired_after={expired_after}"

        return await send_request(endpoint, self.session.token, "delete")

    async def get_all_users_count(self):
        """get all users count.

        **Returns:**
            (int): count of users
        """

        return len(await self.get_users())
