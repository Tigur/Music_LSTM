from collections import Counter
from music21 import *
from .m_classes import *
from formatting import *
from . import options
def split_chords(score):
    for object in score:
        if check_class(object) == MusicLabel.chord :
            chord_offset = object.offset
            chord = object
            score.remove(object)
            for note in chord.notes :
                score.insert(chord_offset, note)

    return True


def check_class(object):
    if isinstance(object, note.Note):
        return MusicLabel.note
    if isinstance(object, chord.Chord):
        return MusicLabel.chord
    if isinstance(object, note.Rest):
        return MusicLabel.rest
    if isinstance(object, tempo.MetronomeMark):
        return MusicLabel.tempo
    if isinstance(object, meter.TimeSignature):
        return MusicLabel.TimeSignature
    if isinstance(object, key.KeySignature):
        return MusicLabel.KeySignature
    else :
        return MusicLabel.other



    return 0



def simplify_tempo(score, one_tempo):
    """ Make score obliged to tempo """

    score.flattenParts()
    score.removeByClass(tempo.MetronomeMark)

    score.insert(0,tempo.MetronomeMark(number = one_tempo.number))



    return score

def check_tempo(score):

    """ Return 5 most common tempos """
    # CAN DEFINITELY REDO THIS :
    # to make it possible to adapt to different tempos in parts.


    all_tempos = [element for element in score.flat.elements if isinstance(element, tempo.MetronomeMark)]
    c = Counter(all_tempos)

    return c.most_common(5)

def presence_of(o_class, score):

    if o_class in score:
        return True
    else :
        return False

def isNeeded(object):
    pass


def get_new_info(score, bin_out = True):
    """
    Parses score flat info with tempo and TimeSignature.
    """
    tempo_list = []
    TimeSignature_list = []
    active_TimeSignature = (binary(0),binary(0))
    active_tempo = binary(0)
    active_TimeSignature_int = (0,0)
    active_tempo_int = 0

    for index,object in enumerate(score,0):
        if check_class(object) == meter.TimeSignature :

            active_TimeSignature = binary(object.numerator), binary(object.denumerator)
            active_TimeSignature_int = object.numerator, object.denumerator
        if check_class(object) == tempo.MetronomeMark:
            active_tempo = binary(object.number)
            active_tempo_int = object.number

        if  options.binary :
            tempo_list.append(active_tempo)
            TimeSignature_list.append(active_TimeSignature)
        else :
            tempo_list.append(active_tempo_int)
            TimeSignature_list.append(active_TimeSignature_int)

    return TimeSignature_list, tempo_list




def prepare(score):
    """
    Transform score into multiDimentional list
    and simplify it's notation, also adding some extra info.
    """


    tempo = check_tempo(score)[0][0]
    simplify_tempo(score,tempo)
    score = score.flat.elements
    #add_new_info(score)

    return score
