import json
from fastapi import WebSocketDisconnect
import os
from random import choice
from string import ascii_uppercase

async def RandomChannelName():
    return ''.join(choice(ascii_uppercase) for i in range(6))

class BaseLayer:
    async def send(self, name, data):
        group = self.get_groups().get(name, {})
        for c in group.values():
            await c.send_text(data)

    async def _receive(self, _group, data):
        try:
            data = json.loads(data)
        except:
            raise "Data must be of dict type"
        await self.receive(_group, data)

    async def group_send_and_exc(self, groupName, channelName, data):
        data = data
        group = self.get_groups().get(groupName, {})
        for c in group.values():
            if not c == channelName:
                await group[c].send_text(data)

    async def send_to_specific_channel(self, groupName, ChannelName, data):
        group = self.get_groups().get(groupName, {})
        assert ChannelName in group.keys(), "No Channel with that name exists"
        await group[ChannelName].send_text(data)

class InMemoryManager(BaseLayer):
    groups = {}
    async def group_add(self, _group, channel, channelName:str = None):
        if channelName and not channelName.isidentifier():
            raise "Channel names must be an identifer"
        group = self.get_groups().setdefault(_group, {})
        name = channelName if channelName else await RandomChannelName()
        group.update({name : channel})
        await self.on_connect(_group, channel)

        try:
            while True:
                data = await channel.receive_text()
                await self._receive(_group, data)
                
        except WebSocketDisconnect:            
            await self.disconnect(_group, name)


    async def group_discard(self, groupName, channelName):
        group = self.get_groups().get(groupName, False)
        if group:
            if group.get(channelName, False):
                del group[channelName]
                if not group:
                    del self.get_groups()[groupName]

    def get_groups(self):
        return self.groups

ChannlsManager = os.environ.get('FASTAPI_SOCKET_MANAGER', InMemoryManager)

class SocketManager(ChannlsManager):
    #on connection, you can close connection with await channel.close()
    async def on_connect(self, group_name, channel):
        await channel.accept()

    #disconnect
    async def disconnect(self, group_name, channelName):
        await self.group_discard(group_name, channelName)

    #receive from websocket
    async def receive(self, group_name, data):
        await self.group_send(group_name, json.dumps(data))

    #receive message from server and send to websocket
    async def group_send(self, group_name, data):
        
        await self.send(group_name, data)

FastSocket = SocketManager()
