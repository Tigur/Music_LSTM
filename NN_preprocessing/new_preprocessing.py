from music21 import *

from collections import Counter
import numpy as np
import enum
import random
from . import options
from .m_classes import *
from .manipulate_score import *
import os
import pdb
import itertools
from misc import *

from formatting import binary




out_path = './t_output/test.mid'

def getRandomFragment(score):
    start = None
    max_start = len(score) - options.fragment_len - 1
    while  start == None or start > max_start :
        start = random.randint(0,max_start)

    out_frag = score[start:start+options.fragment_len]
    fragment = score[start+1:start+options.fragment_len+1]

    return fragment, out_frag

def getFragmentSet(score):
    inSet = []
    outSet = []
    fragmentSet = [getRandomFragment(score) for fragment in range(options.fragment_number)]
    for fragment_pair in fragmentSet:
       inSet.append(fragment_pair[0])
       outSet.append(fragment_pair[1])
    return inSet, outSet

def object_to_food(object):
    #pdb.post_mortem()

    pitch = -1
    duration = -1
    o_class = None
    offset = None
    tempo_one = -1
    TimeSignature = (0,0)

    offset = object.offset
    o_class = check_class(object).value
    if isinstance(object, note.GeneralNote):
        duration = float(object.duration.quarterLength) * 100
    if isinstance(object, note.Note):
        pitch = object.pitch.midi
    if isinstance(object, tempo.MetronomeMark):
        tempo_one = object.number
    if isinstance(object, meter.TimeSignature):
        TSig_n = object.numerator
        TSig_d = object.denominator

    if options.binary :
        input_list = [binary(pitch), binary(duration), binary(o_class), binary(offset)]
    else:
        input_list = [pitch, duration, o_class, offset]
        print(duration)
    return input_list





def fragment_to_food(fragment) :

    ret = [object_to_food(object) for object in fragment]

    return ret

def getFoodPack(score):
    """ Forms a food Pack.
    One pack contains of multiple fragments of food
    First forms a rawPack and then transforms it to food pack
    """

    #score = score.flat # check if it will work
    #split_chords(score)
    #tempo = check_tempo(score)[0][0]
    #simplify_tempo(score,tempo)

    score = prepare(score)


    rawPack = [getRandomFragment(score) for element in range(options.fragment_number)]
    foodPack = [fragment_to_food(fragment) for fragment in rawPack]

    return foodPack

def getLongFood(score):
    score = prepare(score)
    #score = score.flat.elements
    food = []
    TimeSignature, tempo = get_new_info(score, bin_out = False)

    for index, object in enumerate(score,0) :

        food.append(object_to_food(object))
        food[index].append(TimeSignature[index][0])
        food[index].append(TimeSignature[index][1])
        food[index].append(tempo[index])





    if options.fragments :
        food, out = getFragmentSet(food)
        food = np.array(food)
        out = np.array(out)

    return food,out


def make_food(scores):
    """
    scores - A list of all paths to midiFiles.
    """


    if options.longInput :

        food = [getLongFood(score)[0] for score in scores]
        out = [getLongFood(score)[1] for score in scores]
        print(len(food[0]))

      # food = list(itertools.chain.from_iterable(food))
      # out = list(itertools.chain.from_iterable(out))
        food = list(itertools.chain.from_iterable(food))
        out = list(itertools.chain.from_iterable(out))

        return food,out



    else:
        for score in scores :

            print("Packed Food !!! ")

            getFoodPack(score)

        return None

def loadScores(dirpath = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/Inż_repo/MUSIC_PACKAGE/'):

    scores = []

    for fname in os.listdir(dirpath):
        if fname[-4:] not in ('.mid','.MID'):
            continue

        name = fname[:-4]
        current_path = dirpath + fname
        scores.append(converter.parse(current_path))


        print("Loaded {}".format(name))

    return scores


if __name__ == '__main__':

    rel_path = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/Inż_repo/MUSIC_PACKAGE/fav/'

    midiFile = rel_path + 'islamei.mid'
#    midi_to_stateMat(midiFile)
    print(midiFile)

