#!/usr/bin/env python3
import asyncio
import mido
import os
import time
import message
from midi import connect
from functools import partial
from message import Event, parse

class Data:
    def __init__(self) -> None:
        self.messages = {}
        self.midi_out = None
        self.midi_in = None
        
hof_name = "HOF 2"
client_name = 'PedalBoardControl'
port_name = 'midi'
data = Data()
midi = mido.Backend()

def on_message(data:mido.Message):
    type, body = parse(data)
    now = time.time()

    if type is None:
        return
    
    match type:
        case Event.foot.value:
            print(f'{now} - stomp: {body}')
            pass
        case Event.state.value:
            mask = body[0]
            extract_value = lambda a, b, c: body[a] + body[b] * 255 + (127 if mask & c else 0)
            preset = extract_value(1, 2, 0x40)
            level = extract_value(3, 4, 0x10)
            tone = extract_value(5, 6, 0x04)
            decay = extract_value(7, 9, 0x01)
            print(f'{now} - state: level {level} - tone {tone} - decay {decay} - preset {preset} - {message.as_hex_string(body)}')
        case _:
            if not type in data.messages:
                data.messages[type] = body
                print(f'{now} - set {type}: {body}')
            elif data.messages[type] != body:
                data.messages[type] = body
                print(f'{now} - update {type}: {body}')
            else:
                print(f'{now} - {data}')
    
async def main():
    client_name = 'PedalBoardControl'
    port_name = 'midi'
    midi_out = midi.open_output(port_name, client_name=client_name)
    midi_in = midi.open_input(port_name, client_name=client_name, callback=on_message)
    
    connect(midi, client_name, hof_name)
    connect(midi, hof_name, client_name)
    
    ping = message.make([Event.ping.value])
    query = message.make([Event.query.value,24,1,127,127,127])
    
    while True:
        midi_out.send(query)
        await asyncio.sleep(5.0)

try:
    asyncio.run(main())  
except KeyboardInterrupt:
    pass