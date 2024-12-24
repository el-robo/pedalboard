# requirements
- mido
- rtmidi

need fix for
```sh
>>> midi = mido.Backend('mido.backends.rtmidi')
>>> midi_out = midi.open_output('midi')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/eldad/.local/lib/python3.9/site-packages/mido/backends/backend.py", line 117, in open_output
    return self.module.Output(name, **self._add_api(kwargs))
  File "/home/eldad/.local/lib/python3.9/site-packages/mido/ports.py", line 269, in __init__
    BasePort.__init__(self, name, **kwargs)
  File "/home/eldad/.local/lib/python3.9/site-packages/mido/ports.py", line 90, in __init__
    self._open(**kwargs)
  File "/home/eldad/.local/lib/python3.9/site-packages/mido/backends/rtmidi.py", line 198, in _open
    rtapi = _get_api_id(api)
  File "/home/eldad/.local/lib/python3.9/site-packages/mido/backends/rtmidi.py", line 38, in _get_api_id
    return rtmidi.API_UNSPECIFIED
AttributeError: module 'rtmidi' has no attribute 'API_UNSPECIFIED'
```