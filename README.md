# fastapi-websocket-boardcasting
FastApi Websocket parallel broadcasting inspired by django-channels

Simply import the consumer using 

``` from channels import FastSocket ```

to add channel to a group

```
@app.websocket("/{id}")
async def websocket_endpoint(websocket: WebSocket, id):
    name:str = f"group-{id}"
    await FastSocket.group_add(name, websocket)
```

You can specify Channel name:

``` await FastSocket.group_add(name, websocket, "Channel Name") ```

sending to a group

```     await FastSocket.group_send("group-1", json.dumps({"message" : "calling from login"})) ```

Exclude a channel from the group send

```     await FastSocket.group_send_and_exc("group-1", "Channel Name" ,json.dumps({"message" : "calling from login"})) ```

send to specific channel

```     await FastSocket.send_to_specific_channel("group-1", "Channel Name" ,json.dumps({"message" : "calling from login"})) ```

You can override consumer code by importing the manager and create your own consumer

```
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
```
