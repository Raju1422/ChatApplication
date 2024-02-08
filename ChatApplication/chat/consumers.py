from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket connected...",event)
        print("Channel Layer..",self.channel_layer) # to get deafult layer of the project
        print("Channel Name....",self.channel_name) # to get channel name 

        # creating groups 
        async_to_sync(self.channel_layer.group_add)("Lovers",self.channel_name) # it is a async function but we are using it in sync so we are converting  it 
        self.send({
            "type":"websocket.accept"
        })

    def websocket_receive(self,event):
        print("Messsage received from client ...",event)
        print("Message : ",event['text'])
        print("type of message from client .. ",type(event['text']))

        async_to_sync(self.channel_layer.group_send)('Lovers',{
            'type':'chat.message',  # this is passed to chat_message function  it is only for group 
            'message':event['text']
        })
     
    def chat_message(self,event): # this send message to all clients
        print("Event This ...",event)
        print("Data present in ...",event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)

        async_to_sync(self.channel_layer.group_discard)('Lovers',self.channel_name)  # removing the group 

        raise StopConsumer

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Websocket connected...",event)
        print("Channel Layer..",self.channel_layer) # to get deafult layer of the project
        print("Channel Name....",self.channel_name) # to get channel name 

        # creating groups 
        await self.channel_layer.group_add("Lovers",self.channel_name) # it is a async function but we are using it in sync so we are converting  it 
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self,event):
        print("Messsage received from client ...",event)
        print("Message : ",event['text'])
        print("type of message from client .. ",type(event['text']))

        await self.channel_layer.group_send('Lovers',{
            'type':'chat.message',  # this is passed to chat_message function  it is only for group 
            'message':event['text']
        })
     
    async def chat_message(self,event): # this send message to all clients
        print("Event This ...",event)
        print("Data present in ...",event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    async def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)

        await self.channel_layer.group_discard('Lovers',self.channel_name)  # removing the group 

        raise StopConsumer