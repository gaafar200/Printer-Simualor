from enum import Enum
class printerStatus(Enum):
    idle = 1
    printing = 2
    paperJam = 3
    outOfPaper = 4
    offLine = 5
    lowInkOrTunar = 6
    Error = 7
    Busy = 8
    Paused = 9
    cancelled = 10
    unknown = 11