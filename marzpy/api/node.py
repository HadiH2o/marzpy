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

    async def add_node(self, node: Node):
        """add new node.

        Parameters:
            node (``api.Node``): node object

        Returns:
            `~object`: information of new node
        """
        return Node(
            **await send_request(
                endpoint="node", token=self.session.token, method="post", data=node.__dict__
            )
        )

    async def get_node_by_id(self, node_id: int):
        """get exist node from id.

        Parameters:
            node_id (``int``): id of node

        Returns:
            `~object`: information of new node
        """
        return Node(**await send_request(endpoint=f"node/{node_id}", token=self.session.token, method="get"))

    async def modify_node_by_id(self, node_id: int, node: object):
        """edit exist node from id.

        Parameters:
            node_id (``int``): id of node

            node (``api.Node``): node object

        Returns:
            `~object`: information of new node
        """
        request = await send_request(
            endpoint=f"node/{node_id}", token=self.session.token, method="put", data=node.__dict__
        )
        return Node(**request)

    async def delete_node(self, node_id: int):
        """delete node from id.

        Parameters:
            node_id (``int``): id of node

        Returns:
            `~str`: success
        """
        await send_request(endpoint=f"node/{node_id}", token=self.session.token, method="delete")
        return "success"

    async def get_all_nodes(self):
        """get all nodes.

        Returns:
            `~list of objects`: [Node]
        """
        request = await send_request(endpoint="nodes", token=self.session.token, method="get")
        node_list = [Node()]
        for node in request:
            node_list.append(Node(**node))
        del node_list[0]
        return node_list

    async def reconnect_node(self, node_id: int):
        """reconnect from id.

        Parameters:
            node_id (``int``): id of node

        Returns:
            `~str`: success
        """
        request = await send_request(
            endpoint=f"node/{node_id}/reconnect", token=self.session.token, method="post"
        )

        return "success"

    async def get_nodes_usage(self):
        """get all nodes usage.

        Returns:
            `~dict`: "usage" : []
        """
        request = await send_request(endpoint="nodes/usage", token=self.session.token, method="get")
        return request["usages"]

    async def get_nodes_certificate(self):
        """get nodes settings (certificate).

        Returns:
            `~str`: 'certificate'
        """

        request = await send_request(endpoint="node/settings", token=self.session.token, method="get")
        return request["certificate"]
