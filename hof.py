#!/usr/bin/env python3

# from rtmidi.midiutil import open_midioutput, open_midiinput, list_output_ports
# import rtmidi
import asyncio
import mido
import os

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

def on_hof_message(message):
    print(message)
    
async def main():
    client_name = 'PedalBoardControl'
    port_name = 'midi'
    
    midi = mido.Backend()
    midi_out = midi.open_output(port_name, client_name=client_name)
    midi_in = midi.open_input(port_name, client_name=client_name, callback=on_hof_message)
    
    connect(midi, client_name, hof_name)
    connect(midi, hof_name, client_name)
    
    ping = mido.Message('sysex', data=[0,32,31,0,33,5])
    query = mido.Message('sysex', data=[0,32,31,0,33,9,24,1,127,127,127])
    
    while True:
        # await asyncio.sleep(0.1)
        midi_out.send(ping)
        await asyncio.sleep(3.0)

try:
    asyncio.run(main())  
except KeyboardInterrupt:
    pass