import mido
import os

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