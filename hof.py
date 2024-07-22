#!/usr/bin/env python3
import asyncio
import mido
import os
from functools import partial
from enum import Enum

hof_name = "HOF 2"

def find_midi_port(backend:mido.Backend, name:str, input:bool):
    ports = backend.get_input_names() if input else backend.get_output_names()
    print(ports)
    
    for port in ports:
        if name in port:
            return port.split(' ')[-1]
        
def connect(backend:mido.Backend, source, destination):
    source_port = find_midi_port(backend, source, input=True)
    destination_port = find_midi_port(backend, destination, input=False)
    
    if os.system(f'aconnect {source_port} {destination_port}'):
        print(f'could not connect "{source} ({source_port})" to "{destination} ({destination_port})"')
        return False
    
    return True

class Data:
    def __init__(self) -> None:
        self.messages = {}
        
class Event(Enum):
    foot = 15
    state = 8 
    
def as_hex(data:list[int]):
    return ' '.join([f'{value:02X}' for value in data])
        
def on_hof_message(data:Data, message:mido.Message):
    preamble = [0, 32, 31, 0, 33]
    message_data = message.bytes()

    if message_data[1:6] != preamble:
        print(f'unknown preamble: ({message_data[1:6]}) in {message}')
        return
    
    type = message_data[6]
    body = message_data[7:]
    
    match Event(type):
        case Event.foot:
            print(f'stomp: {body}')
            pass
        case Event.state:
            mask = body[0]
            extract_value = lambda a, b, c: body[a] + body[b] * 255 + (127 if mask & c else 0)
            preset = extract_value(1, 2, 0x40)
            level = extract_value(3, 4, 0x10)
            tone = extract_value(5, 6, 0x04)
            decay = extract_value(7, 9, 0x01)
            # print(f'state: level {level} - tone {tone} - decay {decay} - preset {preset} - {as_hex(body)}')
        case _:
            if not type in data.messages:
                data.messages[type] = body
                print(f'set {type}: {body}')
            elif data.messages[type] != body:
                data.messages[type] = body
                print(f'update {type}: {body}')
            else:
                print(message)
    
async def main():
    client_name = 'PedalBoardControl'
    port_name = 'midi'
    data = Data()
    
    midi = mido.Backend()
    midi_out = midi.open_output(port_name, client_name=client_name)
    midi_in = midi.open_input(port_name, client_name=client_name, callback=partial(on_hof_message, data))
    
    connect(midi, client_name, hof_name)
    connect(midi, hof_name, client_name)
    
    ping = mido.Message('sysex', data=[0,32,31,0,33,5])
    query = mido.Message('sysex', data=[0,32,31,0,33,9,24,1,127,127,127])
    
    while True:
        midi_out.send(query)
        await asyncio.sleep(5.0)

try:
    asyncio.run(main())  
except KeyboardInterrupt:
    pass