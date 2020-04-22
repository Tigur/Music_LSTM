import enum


class MusicLabel(enum.Enum):
    note = 0
    chord = 1
    rest = 2
    tempo = 3
    TimeSignature = 4
    KeySignature = 5
    other = 6

