import random
import math
import sys


def new_pitches(low, high):
    pitches = []
    p = 1
    d = high - low  # range of pitches
    x = d - 1
    r = int(random.triangular(0, x, 3))  # random number of notes in the current range
    first_note = high - random.randint(0, d)
    pitches.append(first_note)
    if first_note >= ((low + high) / 2):  # if first note is higher than the middle of the range
        p = -1  # make the first interval downwards
    prev_note = first_note
    for i in range(r):
        new_note = abs(prev_note + math.ceil(random.triangular(0, x, x - 0.5)) * p)
        while new_note < low or new_note > high or new_note in pitches:
            # if the new note is out of range or has already been played,
            # find another note
            new_note = abs(prev_note + math.ceil(random.triangular(0, x, x - 0.5)) * p)
        pitches.append(new_note)
        x = abs(new_note - prev_note) - 1
        if x < 1:
            break  # break after minor second
        prev_note = new_note
        p = -p  # the next interval will be in the opposite direction
    return pitches
