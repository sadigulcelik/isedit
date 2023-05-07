import operator as op
import numpy as np


def _getDurationVex(n, dotted):
    if n not in ["1", "2", "3", "4", "6", "8", "12", "16", "24", "32"]:
        raise Exception("unsupported note length")
    if n == "1":
        res = "w"
    elif n == "2":
        res = "h"
    elif n == "4":
        res = "q"
    else:
        res = n
    if dotted:
        return res + "d"
    return res


def getVexVoices(voices):
    allkeys = []
    alldurations = []
    for voice in voices:
        notes = voice.split(" ")
        keys = []
        freqs = []
        durations = []
        notelst = list("c-d-ef-g-a-b")
        for note in notes:
            if len(note) == 0:
                continue
            rest = list(note[1:])
            sharp = 0
            for i in range(1, len(note)):
                if i + 1 < len(note):
                    if note[i : i + 2] == "is":
                        sharp += 1
                    elif note[i : i + 2] == "es":
                        sharp -= 1
            key = note[0]

            octave = 3 + op.countOf(rest, "'") - op.countOf(rest, ",")

            if sharp == 0:
                key += "n"
            elif sharp == 1:
                key += "#"
            elif sharp == 2:
                key += "##"
            elif sharp == -1:
                key += "@"
            elif sharp == -2:
                key += "@@"
            else:
                raise Exception("multiple sharps not supported")

            key += "/" + str(int(octave))
            keys.append(key)

            i = len(note) - 1

            dotted = False

            if note[i] == ".":
                dotted = True
                i -= 1
            if note[i] == ".":
                raise Exception("multiple dots not supported")

            base_duration = ""

            nums = "0123456789"

            while note[i] in nums:
                base_duration = note[i] + base_duration
                i -= 1

            dur = _getDurationVex(base_duration, dotted)

            durations.append(dur)

        allkeys.append(keys)
        alldurations.append(durations)

    return allkeys, alldurations
