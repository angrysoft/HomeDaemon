import asyncio
import websockets
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue, url='192.168.1.4', port=9000):
        super(Input, self).__init__(queue)
        self.name = 'websocket'
        self.url = url
        self.port = port
        self.clients = set()
        self.server = self.loop.run_until_complete(websockets.serve(self._handler, self.url, self.port))

    async def _handler(self, websocket, path):
        await self._register(websocket)
        try:
            async for message in websocket:
                self.queue.put(message)
        finally:
            await self._unregister(websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.remove(client)

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])

