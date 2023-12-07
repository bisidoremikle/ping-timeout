import math

from scamp import *
import sys
import random
import algorithm

s = Session()
# s.fast_forward_to_beat(55)  # 2 part (retrograde)
# s.fast_forward_to_beat(119)  # 3 part (intervals)
# s.fast_forward_to_beat(200)  # 4 part (now_pitch)
# s.fast_forward_to_beat(400)  # 5 part (chords and filters)
# s.fast_forward()

# s.print_available_midi_output_devices()

pitches = []
dur = []
a_dur = []
a_pitches = []
p_dur = []
p_pitches = []
cc_arr = []
dist_arr = []
now_pitch = []
now_dur = []
# seed = random.randrange(sys.maxsize)  # use it to make new random seed
# seed = 7058047395806553335 1173009000433458687 4834867942578893545
# seed = 1173009000433458687  # try this too
seed = 4834867942578893545
random.seed(seed)
print("Seed was: ", seed)
low = 61
high = 66
min = 30  # lowest note
max = 88  # highest note

while len(pitches) < 60:  # 60 music phrases
    durations = []
    if low > min:
        low = math.ceil(low - 0.1 * len(pitches))  # low limit gets lower
    if high < max:
        high = math.floor(high + 0.1 * len(pitches))  # high limit gets higher
    new_pitch = algorithm.new_pitches(low, high)  # generate notes by the algorithm
    pitches.append(new_pitch)
    for i in new_pitch:
        durations.append(0.25 / random.uniform(1, len(pitches) / 10 + 0.01))  # decreasing durations
    dur.append(durations)
    pitches.append([None])  # add a rest between phrases
    dur.append([random.uniform(1,3) / random.uniform(1, len(pitches)/10 + 0.01)])

print(pitches)
print(dur)

flat_dur = [item for sublist in dur for item in sublist]  # make a list of all durations
double_flat = flat_dur.copy()  # make a copy to keep original list untouched
double_pitches = pitches.copy()
random.shuffle(double_flat)  # shuffle pitches in random order
random.shuffle(double_pitches)  # shuffle durations in another random order
flat_pitches = [item for sublist in double_pitches for item in sublist]
print("Flat pitches is ", flat_pitches)
# create MIDI channels
piano = s.new_midi_part("piano", midi_output_device=1, num_channels=15)
acc = s.new_midi_part("accordion", midi_output_device=2, num_channels=15)
double_piano = s.new_midi_part("double_piano", midi_output_device=3, num_channels=15)
double_acc = s.new_midi_part("double_acc", midi_output_device=4, num_channels=15)

for i in range(len(pitches)):
    for j in range(len(pitches[i])):
        r = random.random()
        cc = 'param_12: ' + str(r)  # some random synth parameters for each note
        dist = 'param_63: ' + str(r)
        if pitches[i][j] is None:
            p = None
            d = dur[i][j] / random.randint(1, 3)  # divide a rest
        else:
            p = pitches[i][j]
            d = dur[i][j]
        # print(p, d)
        p_dur.append(d)
        p_pitches.append(p)
        cc_arr.append(cc)
        dist_arr.append(dist)
counter = 0
for i in range(len(pitches)):
    for j in range(len(pitches[len(pitches) - i - 1])):  # pitches in reversed order
        r = random.random()
        cc = 'param_12: ' + str(r)
        dist = 'param_63: ' + str(r)
        if pitches[len(pitches) - i - 1][len(pitches[len(pitches) - i - 1]) - j - 1] is None:
            p = None
            d = flat_dur[counter] / random.randint(1, 3)
        else:
            p = pitches[len(pitches) - i - 1][len(pitches[len(pitches) - i - 1]) - j - 1]
            d = flat_dur[counter]
        p_dur.append(d)
        p_pitches.append(p)
        cc_arr.append(cc)
        dist_arr.append(dist)
        counter += 1

for i in range(len(pitches)):
    for j in range(len(pitches[i])):
        if pitches[i][j] is None:
            p = None
            d = dur[i][j] / random.randint(1, 3)  # the accordion gets another random rests
        else:
            p = pitches[i][j]
            d = dur[i][j]
        # print(p, d)
        a_dur.append(d)
        a_pitches.append(p)
counter = 0
for i in range(len(pitches)):
    for j in range(len(pitches[len(pitches) - i - 1])):
        if pitches[len(pitches) - i - 1][len(pitches[len(pitches) - i - 1]) - j - 1] is None:
            p = None
            d = flat_dur[counter] / random.randint(1, 3)  # and random rests for the retrograde part
        else:
            p = pitches[len(pitches) - i - 1][len(pitches[len(pitches) - i - 1]) - j - 1]
            d = flat_dur[counter]
        a_dur.append(d)
        a_pitches.append(p)
        counter += 1
# b_pitches = list(a_pitches[0:423])
# b_dur = list(a_dur[0:423])
print ("a_pitches is ", a_pitches)
# print ("b_pitches is ", b_pitches)
print("len(a_pitches) is ", len(a_pitches))

def one():
    for i in range(len(p_pitches)):
        print("Synth pitch: ", p_pitches[i], " duration: ", p_dur[i])
        piano.play_note(p_pitches[i], 1.0, p_dur[i], [cc_arr[i], dist_arr[i]])


def two():
    global now_pitch, now_dur
    acc.play_note(None, 1.0, 1)  # quarter rest
    big_pause = sum(a_dur)
    # acc.play_note(None, 1.0, big_pause)
    for i in range(len(a_pitches)):
        print("Bayan pitch: ", a_pitches[i], " duration: ", a_dur[i])
        acc.play_note(a_pitches[i], 1.0, a_dur[i])
    counter = 0
    print("Double flat is ", double_flat)
    for i in range(len(double_pitches)):  # shuffled pitches and durations in reverse order
        for j in range(len(double_pitches[len(double_pitches) - i - 1])):
            note = double_pitches[len(double_pitches) - i - 1][len(double_pitches[len(double_pitches) - i - 1]) - j - 1]
            if note is None:
                p = None
                d = double_flat[counter]
            else:
                p = note
                d = double_flat[counter]
            if d < 0.1:
                d = d * d * d
            if d >= 0.1:
                print("Bayan pitch: ", p, " duration: ", d)
                acc.play_note(p, 1.0, d)
            counter += 1
    acc.play_note(None, 1.0, 5)  # 5 bars rest
    print("Starting now_pitch")
    for i in range(len(now_dur)):  # receive pitches from a synth
        p = now_pitch[i]
        print("Bayan pitch: ", p, " duration: ", now_dur[i])
        acc.play_note(p, 1.0, now_dur[i])
    for i in range(len(now_dur)):  # receive pitches from a synth again
        p = now_pitch[i]
        print("Bayan pitch: ", p, " duration: ", now_dur[i])
        acc.play_note(p, 1.0, now_dur[i])
    acc.play_note(None, 1.0, 5)
    # print(now_pitch)
    chords = [[4, 7], [3, 6], [4, 9], [4, 10], [3, 7]]  # 5 chords to choice
    for i in range(int(len(now_pitch) / 2 + len(chords))):
        if now_pitch[i] is None or now_pitch[i] > 48:  # keep only low pitches
            print("Bayan pitch: None", " duration: ", now_dur[i])
            acc.play_note(None, 1.0, now_dur[i])  # and convert to rests all that remains
        else:
            r = random.randint(0, len(chords) - 1)
            note = now_pitch[i]
            print("Bayan pitches: ", [note, note + chords[r][0], note + chords[r][1]], " duration: ", now_dur[i] + r)
            acc.play_chord([note, note + chords[r][0], note + chords[r][1]], 1.0, now_dur[i] + r)



def three():  # double synth
    global now_pitch, now_dur
    for i in range(len(p_dur)):
        double_piano.play_note(None, 1.0, p_dur[i])
    # double voices with shuffled arrays
    counter = 0
    for i in range(len(double_pitches)):
        for j in range(len(double_pitches[len(double_pitches) - i - 1])):
            r = random.random()
            cc = 'param_12: ' + str(r)
            dist = 'param_63: ' + str(r)
            note = double_pitches[len(double_pitches) - i - 1][len(double_pitches[len(double_pitches) - i - 1]) - j - 1]
            if note is None:
                p = None
                d = double_flat[len(double_flat) - counter - 1] * 4
            else:
                p = note + random.randrange(-12, 12) * 2  # add a whole tone interval
                d = double_flat[counter] + double_flat[len(double_flat) - counter - 1]
            if d < 1:
                d = d * random.randrange(1,3)
            now_pitch.append(p)  # translate the pitch to the accordion
            now_dur.append(d)
            print("Synth pitch: ", p, " duration: ", d)
            double_piano.play_note(p, 1.0, d, [cc, dist])
            counter += 1
    double_piano.play_note(None, 1.0, 20)  # 5 bars rest
    print("Flat pitches section")
    for i in range(len(flat_pitches)):
        if flat_pitches[i] is None:  # ignore rests
            continue
        r = random.random()
        cc = 'param_12: ' + str(r)
        dist = 'param_63: ' + str(r)
        note = flat_pitches[i]
        if i < 50:
            add = 0
        else:
            add = i/20
        # if 48 < note <= 72:
        if 44 < note <= 76:  # keep only low and high pitches
            p = None  # and convert to rests all that remains
            d = double_flat[i]
        else:
            p = note
            d = double_flat[i] + 2 + add  # increase durations
        print("Synth pitch: ", p, " duration: ", d)
        double_piano.play_note(p, 0.1, d, [cc, dist])


def four():  # double acc
    double_acc.play_note(None, 1.0, 1)
    # normal order
    for i in range(len(a_dur)):
        acc.play_note(None, 1.0, a_dur[i])
    # double voices with shuffled arrays
    counter = 0
    for i in range(len(double_pitches)):
        for j in range(len(double_pitches[len(double_pitches) - i - 1])):
            note = double_pitches[len(double_pitches) - i - 1][len(double_pitches[len(double_pitches) - i - 1]) - j - 1]
            if note is None:
                p = None
                d = double_flat[counter]
            else:
                p = note + random.randint(-6, 6) * 2  # add a whole tone interval
                d = double_flat[counter]
            if d < 0.1:
                d = d*d*d
            # print(d)
            print("Bayan second pitch: ", p)
            double_acc.play_note(p, 1.0, d)
            counter += 1


s.fork(one)
s.fork(two)
s.fork(three)
s.fork(four)
s.start_transcribing()
s.wait_for_children_to_finish()
performance = s.stop_transcribing()
performance.to_score(
    title="ping timeout",
    composer="Mikhail Puchkov",
    simplicity_preference=4
).show()
