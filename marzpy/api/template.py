from typing import List

from .send_requests import *


class Template:
    def __init__(
            self,
            name="",
            inbounds={},
            data_limit={},
            expire_duration=0,
            username_prefix="",
            username_suffix="",
            id=None,
    ):
        self.name = name
        self.inbounds = inbounds
        self.data_limit = data_limit
        self.expire_duration = expire_duration
        self.username_prefix = username_prefix
        self.username_suffix = username_suffix
        self.id = id


class TemplateMethods:
    def __init__(self, session):
        self.session = session

    async def get_all_templates(self) -> List[Template]:
        """get all templates list.

        **Returns:**
            (List[Template]): list of templates
        """
        request = await send_request(endpoint="user_template", token=self.session.token, method="get")
        template_list = [Template()]
        for user in request:
            template_list.append(Template(**user))
        del template_list[0]
        return template_list

    async def add_template(self, template: Template) -> Template:
        """add new template.

        **Parameters:**
            * `template` (Template) : Template information

        **Returns:**
            (Template) : information of new template
        """
        request = await send_request(endpoint="user_template", token=self.session.token, method="post", data=template.__dict__)
        return Template(**request)

    async def get_template_by_id(self, template_id: int):
        """get exist template from id.

        **Parameters:**
            `template_id` (id) : template id

        **Returns:**
            (Template) : information of template
        """
        request = await send_request(
            endpoint=f"user_template/{template_id}", token=self.session.token, method="get"
        )

        return Template(**request)

    async def modify_template_by_id(self, template_id: int, template: Template):
        """edit exist template from id.

        **Parameters:**
            * `template_id` (id) : template id
            * `template` (Template) : new template information

        **Returns:**
            (Template) : information of modified template
        """
        request = await send_request(endpoint=f"user_template/{template_id}", token=self.session.token, method="put", data=template.__dict__)
        return Template(**request)

    async def delete_template_by_id(self, template_id: int):
        """delete template from id.

        **Parameters:**
            * `template_id` (id) : template id

        **Returns:**
            (str) : success
        """
        await send_request(endpoint=f"user_template/{template_id}", token=self.session.token, method="delete")
        return "success"
