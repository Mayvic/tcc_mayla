from dataclasses import dataclass
@dataclass
class ambiente:
    coord: str
    trace: str
    exitFile: str
    wall: bool

ambiente1 = ambiente('10mil/pos-10000-20-20-1-7-9-0-1-1','10mil/trace-10000-20-20-1-7-9-0-1-1','data/fingerprints1', False);
ambiente3 = ambiente('10mil/pos-10000-20-20-3-7-9-0-1-1','10mil/trace-10000-20-20-3-7-9-0-1-1','data/fingerprints3', True);

usedAmbiente = ambiente3
