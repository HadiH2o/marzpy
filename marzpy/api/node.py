from typing import List

from .send_requests import *


class Node:
    def __init__(
            self,
            name="",
            address="",
            port=62050,
            api_port=62051,
            xray_version="",
            add_as_new_host=False,
            certificate="",
            id=0,
            status="",
            message="",
            usage_coefficient=1,
    ):
        self.name = name
        self.address = address
        self.port = port
        self.api_port = api_port
        self.xray_version = xray_version
        self.add_as_new_host = add_as_new_host
        self.certificate = certificate
        self.id = id
        self.status = status
        self.message = message
        self.usage_coefficient = usage_coefficient


class NodeMethods:
    def __init__(self, session) -> None:
        self.session = session

    async def add_node(self, node: Node) -> Node:
        """add new node.

        **Parameters:**
            * `node` (Node): node object

        **Returns:**
            (Node): information of new node

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeInvalidEntity` : node information is invalid
        """
        response = await send_request(endpoint="node", token=self.session.token, method="post", data=node.__dict__)
        return Node(**response)

    async def get_node(self, node_id: int) -> Node:
        """get exist node from id.

        **Parameters:**
            * `node_id` (int): id of node

        **Returns:**
            (Node): information of node

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeNotFound` : node not found
            * `NodeInvalidEntity` : node information is invalid
        """
        return Node(**await send_request(endpoint=f"node/{node_id}", token=self.session.token, method="get"))

    async def modify_node(self, node_id: int, node: object) -> Node:
        """edit exist node from id.

        **Parameters:**
            * `node_id` (int): id of node
            * `node` (Node): node object

        **Returns:**
            (Node): information of new node

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeNotFound` : node not found
            * `NodeInvalidEntity` : node information is invalid
        """

        request = await send_request(
            endpoint=f"node/{node_id}", token=self.session.token, method="put", data=node.__dict__
        )
        return Node(**request)

    async def delete_node(self, node_id: int) -> str:
        """delete node from id.

        **Parameters:**
            * node_id (int): id of node

        **Returns:**
            (str): success

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeNotFound` : node not found
            * `NodeInvalidEntity` : node information is invalid
        """
        await send_request(endpoint=f"node/{node_id}", token=self.session.token, method="delete")
        return "success"

    async def get_nodes(self) -> List[Node]:
        """get all nodes.

        **Returns:**
            (List[Node]): list of nodes

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
        """
        request = await send_request(endpoint="nodes", token=self.session.token, method="get")
        node_list = [Node(**node) for node in request]
        return node_list

    async def reconnect_node(self, node_id: int) -> str:
        """reconnect from id.

        **Parameters:**
            * `node_id` (int): id of node

        **Returns:**
            (str): success

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeNotFound` : node not found
            * `NodeInvalidEntity` : node information is invalid
        """
        request = await send_request(endpoint=f"node/{node_id}/reconnect", token=self.session.token, method="post")
        return "success"

    async def get_nodes_usage(self):
        """get all nodes' usage.

        **Returns:**
            (dict): {"usage" : []}

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this
            * `NodeInvalidEntity` : node information is invalid
        """
        request = await send_request(endpoint="nodes/usage", token=self.session.token, method="get")
        return request["usages"]

    async def get_nodes_certificate(self):
        """get nodes settings (certificate).

        Returns:
            (str): 'certificate'

        **Raises:**
            * `NotAuthorized` : you are not authorized to do this

        """

        request = await send_request(endpoint="node/settings", token=self.session.token, method="get")
        return request["certificate"]
