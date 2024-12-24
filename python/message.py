from enum import Enum
import mido

class Device(Enum):
    hall_of_fame_2 = 0x21

class Event(Enum):
    probe = 0x03
    ping = 0x05
    state = 0x08
    query = 0x09
    start_preset = 0x1E
    preset = 0x0D
    foot = 0x0F

preset_size = 147

def header(device:Device = Device.hall_of_fame_2):
    return [0x00, 0x20, 0x1F, 0x00, device.value]
    
def as_hex_string(data:list[int]):
    return ', '.join([f'0x{value:02X}' for value in data])
    
def from_hex_string(string:str) -> list[int]:
    parts = string.split(', ')
    return [int(part[2:], 16) for part in parts]

def parse(message:mido.Message, device:Device = Device.hall_of_fame_2):
    preamble = header(device)
    message_data = message.bytes()
    
    if len(message_data) < len(preamble) + 2:
        return None, None

    if message_data[1:6] != preamble:
        return None, None
    
    type = message_data[6]
    body = message_data[7:-1]

    return type, body

def make(body:list[int], device:Device = Device.hall_of_fame_2):
    data = header(device)
    data.extend(body)
    return mido.Message('sysex', data=data)
