#!/usr/bin/env python3.6

import sys
import asyncio
import websockets
import datetime


def prepare_msg_to_send(msg):
	new_msg = "send time: "+"{}\n".format(datetime.datetime.now())
	new_msg += "msg: " + msg
	return new_msg


async def msg():
	async with websockets.connect('ws://localhost:8765') as websocket:
		while True:
			send_msg = input("> ")
			await websocket.send(prepare_msg_to_send(send_msg))
			msg  = await websocket.recv()
			print(msg)



if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(msg())
	asyncio.get_event_loop().run_forever()
