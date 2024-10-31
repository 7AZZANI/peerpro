# file_sharing/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .networking import discover_peers, connect_to_peer, receive_connection
from .file_transfer import send_file

class FileShareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'discover_peers':
            peers = await discover_peers()
            await self.send(text_data=json.dumps({
                'action': 'peer_list',
                'peers': peers
            }))
        elif action == 'connect_to_peer':
            peer_ip = text_data_json['peer_ip']
            success = await connect_to_peer(peer_ip)
            if success:
                await self.send(text_data=json.dumps({
                    'action': 'connection_request',
                    'peer_ip': peer_ip
                }))
            else:
                await self.send(text_data=json.dumps({
                    'action': 'connection_response',
                    'success': False,
                    'peer_ip': peer_ip
                }))
        elif action == 'connection_response':
            peer_ip = text_data_json['peer_ip']
            success = text_data_json['success']
            await receive_connection(peer_ip, success)
            await self.send(text_data=json.dumps({
                'action': 'connection_response',
                'success': success,
                'peer_ip': peer_ip
            }))
        elif action == 'send_file':
            peer_ip = text_data_json['peer_ip']
            file_data = text_data_json['file_data']
            success = await send_file(peer_ip, file_data)
            await self.send(text_data=json.dumps({
                'action': 'file_transfer_status',
                'success': success,
                'peer_ip': peer_ip
            }))