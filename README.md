# marzpy

A Python library that helps you easily use [Marzban](https://github.com/Gozargah/Marzban)'s API panel
> [!IMPORTANT]
> **Status:** Working on new update 🔥

## installation

```shell
pip install marzpy
```

requirements : ```aiohttp```

# How To Use

```python
from marzpy import Marzban, Session
import asyncio


async def main():
    session = Session("username", "password", "https://example.com")
    await session.start_session()

    panel = Marzban(session)
    # await await panel.anyfunction()


asyncio.run(main())

```

# Features

- Admin
    - [get token](#get-token)
    - [get admin](#get-current-admin)
    - [create admin](#create-admin)
    - [modify admin](#modify-admin)
    - [remove admin](#remove-admin)
    - [get admins](#get-admins)
- Subscription
    - [user subscription](#user-subscription)
    - [user subscription info](#user-subscription-info)
- System
    - [get system stats](#get-system-stats)
    - [get inbounds](#get-inbounds)
    - [get hosts](#get-hosts)
    - [modify hosts](#modify-hosts)
- Core
    - [get core stats](#get-core-stats)
    - [restart core](#restart-core)
    - [get core config](#get-core-config)
    - [modify core config](#modify-core-config)
- User
    - [add user](#add-user)
    - [get user](#get-user)
    - [modify user](#modify-user)
    - [delete user](#delete-user)
    - [reset user data usage](#reset-user-data-usage)
    - [reset all users data usage](#reset-all-users-data-usage)
    - [get users](#get-users)
    - [get user usage](#get-user-usage)
    - [get_expired_users](#get-expired-users)
    - [delete_expired_users](#delete-expired-users)
- User Template
    - [get all user templates](#get-all-user-templates)
    - [add user template](#add-user-template)
    - [get user template](#get-user-template)
    - [modify user template](#modify-user-template)
    - [remove user template](#remove-user-template)
- Node
    - [add node](#add-node)
    - [get node](#get-node)
    - [modify node](#modify-node)
    - [remove node](#remove-node)
    - [get nodes](#get-nodes)
    - [reconnect node](#reconnect-node)
    - [get all nodes usage](#get-node-usage)
    - [get nodes certificate](#get-nodes-certificate)

## Thanks To

- [ErfanTech](https://github.com/ErfanTech) :laughing:
- [HadiH2o](https://github.com/HadiH2o) 😭

# Examples

### Get Token

```python

from marzpy import Marzban, Session

session = Session("username", "password", "https://example.com")
my_token = await session.start_session()

panel = Marzban(session)
my_token = await panel.get_token(panel_address, username, password)

```

### Get Current admin

```python
admin = await panel.get_current_admin()
print(admin)  # output: {'username': 'admin', 'is_sudo': True}
```

### Create Admin

```python
admin = Admin(username='username', is_sudo=True, password='password')
result = await panel.create_admin(admin=admin)
print(result)  # output: success
```

### Modify Admin

```python
target_admin = "test"
admin = Admin(username=target_admin, is_sudo=True, password='password')
result = await panel.modify_admin(username=target_admin, admin=admin)
print(result)  # output: success
```

### Remove Admin

```python
target_admin = "test"
result = await panel.delete_admin(username=target_admin)
print(result)  # output: success
```

### Get Admins

```python
result = await panel.get_admins()
print(result)
# output: [{'username': 'test', 'is_sudo': True}, {'username': 'test1', 'is_sudo': False}]
```

### User Subscription

```python
subscription_url = "https://sub.yourdomain.com/sub/eyJhbGciOiJIUzI8NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJNbWRDcmFaeSIsImFjY2VzcyI8InN1YnNjcmlwdGlvbiIsImlhdCI1MTY5NDk1NTkxMH0.o75ML5835SPXpVPKXcvEIUxMTwSy-4XGS9NIdWOAmXY"
result = await panel.get_subscription(subscription_url)
print(result)  # output: Configs
```

### User Subscription info

```python
subscription_url = "https://sub.yourdomain.com/sub/eyJhbGciOiJIUzI8NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJNbWRDcmFaeSIsImFjY2VzcyI8InN1YnNjcmlwdGlvbiIsImlhdCI1MTY5NDk1NTkxMH0.o75ML5835SPXpVPKXcvEIUxMTwSy-4XGS9NIdWOAmXY"
result = await panel.get_subscription_info(subscription_url)
print(result)  # output: User information (usage,links,inbounds,....)
```

### Get System Stats

```python
result = await panel.get_system_stats()
print(result)  # output: system stats Memory & CPU usage ...
```

### Get Inbounds

```python
result = await panel.get_inbounds()
print(result)  # output: list of inbounds
```

### Get Hosts

```python
result = await panel.get_hosts()
print(result)  # output: list of hosts
```

### Modify Hosts

```python
hosts = {
    "VMess TCP": [
        {
            "remark": "somename",
            "address": "someaddress",
            "port": 0,
            "sni": "somesni",
            "host": "somehost",
            "security": "inbound_default",
            "alpn": "",
            "fingerprint": ""
        }
    ]
}
# **Backup first**
result = await panel.modify_hosts(data=hosts)
print(result)  # output: hosts
```

### Get Core Stats

```python
result = await panel.get_xray_core()
print(result)
# output: {'version': '1.8.1', 'started': True, 'logs_websocket': '/api/core/logs'}
```

### Restart Core

```python
result = await panel.restart_xray_core()
print(result)
# output: success
```

### Get Core Config

```python
result = await panel.get_xray_config()
print(result)  # output: your xray core config
```

### Modify Core Config

```python
new_config = {"your config"}
result = await panel.modify_xray_config(config=new_config)
print(result)  # output: success
```

### Add User

```python
from marzpy.api.user import User

user = User(
    username="Mewhrzad",
    proxies={
        "vmess": {"id": "35e7e39c-7d5c-1f4b-8b71-508e4f37ff53"},
        "vless": {"id": "35e7e39c-7d5c-1f4b-8b71-508e4f37ff53"},
    },
    inbounds={"vmess": ["VMess TCP"], "vless": ["VLESS TCP REALITY"]},
    expire=0,
    data_limit=0,
    data_limit_reset_strategy="no_reset",
)
result = await panel.add_user(user=user)  # return new User object

print(result.username)
# -> Mewhrzad, #user.proxies, #user.inbounds, #user.expire, #user.data_limit, #userdata_limit_reset_strategy, #user.status, #user.used_traffic, #user.lifetime_used_traffic, #user.created_at, #user.links, #user.subscription_url, #user.excluded_inbounds
```

### Get User

```python
result = await panel.get_user(user_username="Mewhrzad")  # return User object
print(result.subscription_url)
```

### Modify User

```python
new_user = User(
    username="test",
    proxies={
        "vmess": {"id": "35e4e39c-7d5c-4f4b-8b71-558e4f37ff53"},
        "vless": {"id": "35e4e39c-7d5c-4f4b-8b71-558e4f37ff53"},
    },
    inbounds={"vmess": ["VMess TCP"], "vless": ["VLESS TCP REALITY"]},
    expire=0,
    data_limit=0,
    data_limit_reset_strategy="no_reset",
    status="active",
)
result = await panel.modify_user(user_username="Mewhrzad", user=new_user)
print(result.subscription_url)  # output: modified user object
```

### Delete User

```python
result = await panel.delete_user(user_username="test")
print(result)  # output: success
```

### Reset User Data Usage

```python
result = await panel.reset_user_traffic(user_username="test")
print(result)  # output: success
```

### Reset All Users Data Usage

```python
result = await panel.reset_all_users_traffic()
print(result)  # output: success
```

### Get Users

```python
result = await panel.get_users()  # return list of users
for user in result:
    print(user.username) 
```

### Get User Usage

```python
result = await panel.get_user_usage(user_username="mewhrzad")
print(result)
# output: [{'node_id': None, 'node_name': 'MTN', 'used_traffic': 0}, 
# {'node_id': 1, 'node_name': 'MCI', 'used_traffic': 0}]
```

### Get Expired Users

```python
result = await panel.get_expired_users()
print(result)
```

### Delete Expired Users

```python
result = await panel.delete_expired_users()
print(result)
```

### Get All User Templates

```python
result = await panel.get_templates()  # return template list object
for template in result:
    print(template.name)
```

### Add User Template

```python
from marzpy.api.template import Template

temp = Template(
    name="new_template",
    inbounds={"vmess": ["VMESS TCP"], "vless": ["VLESS TCP REALITY"]},
    data_limit=0,
    expire_duration=0,
    username_prefix=None,
    username_suffix=None,
)
result = await panel.add_template(template=temp)  # return new Template object
print(result.name)  # output: new_template
```

### Get User Template

```python
template_id = 11
result = await panel.get_template(template_id=template_id)  # return Template object
print(result.name)  # output: new_template
```

### Modify User Template

```python
from marzpy.api.template import Template

temp = Template(
    name="new_template2",
    inbounds={"vmess": ["VMESS TCP"], "vless": ["VLESS TCP REALITY"]},
    data_limit=0,
    expire_duration=0,
    username_prefix=None,
    username_suffix=None,
)
result = await panel.modify_template(template_id=1, template=temp)  # return Modified Template object
print(result.name)  # output: new_template2
```

### Remove User Template

```python
result = await panel.delete_template(template_id=1)
print(result)  # output: success
```

### Add Node

```python
from marzpy.api.node import Node

my_node = Node(
    name="somename",
    address="test.example.com",
    port=62050,
    api_port=62051,
    certificate="your_cert",
    id=4,
    xray_version="1.8.1",
    status="connected",
    message="string",
)

result = await panel.add_node(node=my_node)  # return new Node object
print(result.address)
```

### Get Node

```python
result = await panel.get_node(node_id=1)  # return exist Node object
print(result.address)  # output: address of node 1
```

### Modify Node

```python
from marzpy.api.node import Node

my_node = Node(
    name="somename",
    address="test.example.com",
    port=62050,
    api_port=62051,
    certificate="your_cert",
    id=4,
    xray_version="1.8.1",
    status="connected",
    message="string",
)

result = await panel.modify_node(node_id=1, node=my_node)  # return modified Node object
print(result.address)  # output:test.example.com
```

### Remove Node

```python
result = await panel.delete_node(node_id=1)
print(result)  # output: success
```

### Get Nodes

```python
result = await panel.get_nodes()  # return List of Node object
for node in result:
    print(node.address)
```

### Reconnect Node

```python
result = await panel.reconnect_node(node_id=1)
print(result)  # output: success
```

### Get Node Usage

```python
result = await panel.get_nodes_usage()
for node in result:
    print(node)
# output:{'node_id': 1, 'node_name': 'N1', 'uplink': 1000000000000, 'downlink': 1000000000000}
# {'node_id': 2, 'node_name': 'N2', 'uplink': 1000000000000, 'downlink': 1000000000000}
```

### Get Nodes Certificate

```python
result = await panel.get_nodes_certificate()
# output: string
```
