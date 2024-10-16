from dataclasses import dataclass
@dataclass
class ambiente:
    coord: str
    trace: str
    exitFile: str
    wall: bool

ambiente1 = ambiente('pos-1000-20-20-1-7-9-0-1-1','trace-1000-20-20-1-7-9-0-1-1','fingerprints1', False);
ambiente3 = ambiente('pos-1000-20-20-3-7-9-0-1-1','trace-1000-20-20-3-7-9-0-1-1','fingerprints3', True);

usedAmbiente = ambiente3
