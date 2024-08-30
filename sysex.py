#!/usr/bin/env python3
import asyncio
import mido
import message
import json
import sys
from midi import connect
from message import Event, as_hex_string, from_hex_string

sysex = { 
    'responses': {},
    'requests': []
}

try:
    with open('sysex.json', 'r') as file:
        sysex = json.load(file)
        print('read sysex.json')
except FileNotFoundError:
    print('starting from scratch I see')

record_mode = False
running = True
store_response_for_request = None

if len(sys.argv) > 1 and sys.argv[1] == 'read':
    record_mode = True

client_name = 'SysexRecorder'
hof_name = "HOF 2"
port_name = 'midi'
midi = mido.Backend()
midi_out = midi.open_output(port_name, client_name=client_name)

def save():
    with open('sysex.json', 'w') as file:
        json.dump(sysex, file, indent=2)
        print('wrote sysex.json')

def on_message(data:mido.Message):
    global running
    global record_mode
    global store_response_for_request
    global sysex
    global midi_out
    
    try:
        type, body = message.parse(data)
        command = as_hex_string(data.bytes()[1:-1])
        # print(f'<unknown>: {command}')
        
        if type is None:
            # print(f'<unknown>: {command}')
            return
        
        if record_mode:
            if command not in sysex['responses'] and command not in sysex['requests']:
                print(f'new request: {command} / {data}')
                sysex['requests'].append(command)
                running = False
            else:
                print(f'have response(s), sending them')
                for response in sysex['responses'][command]:
                    data = mido.Message('sysex', data=from_hex_string(response))
                    print(f'writing {data}')
                    midi_out.send(data)
                
        elif store_response_for_request is not None:
            sysex['responses'].get(store_response_for_request,[]).append(command)
            save()
            print(f'got response for request: {command}')
        else:
            print(f'<ignore>: {command}')
            
    except Exception as e:
        running = False
        print(e)        

midi_in = midi.open_input(port_name, client_name=client_name, callback=on_message)

async def main():
    global record_mode
    global store_response_for_request
    
    if not record_mode:
        connect(midi, client_name, hof_name)
        connect(midi, hof_name, client_name)

        await asyncio.sleep(1)
        
        if not len(sysex['requests']):
            print('nothing to request')
            return
        
        command = sysex['requests'][-1]
        sysex['responses'][command] = []
        store_response_for_request = command        
        print(f'sending {command}: {from_hex_string(command)}')
        message = mido.Message('sysex', data=from_hex_string(command))
        print(f'writing {message}')
        midi_out.send(message)
    
    while running:
        await asyncio.sleep(1.0)

try:
    asyncio.run(main())  
except KeyboardInterrupt:
    pass

save()