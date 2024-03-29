import tempfile
import os
import subprocess
import operator as op
from IPython.display import Image
import shutil
import numpy as np
import pyaudio
import config
import deprecation
from midiutil import MIDIFile
import pygame
from .VexConversion import getVexVoices
import ipywidgets as widgets
from .ipyscore import Ipyscore
from ipywidgets import Layout


""" Helper function to generate file from voices and time signature

Parameters
----------
voices : list
    List of voices, where each voice is in lilypond formatting
time_signature : string
    The time signature

"""


def _FileGenerator(voices, time_signature):
    linebr = """
"""
    ly_output = """\\version "2.24.1"
\\paper {
  indent = 0\\mm
  line-width = 110\\mm
  oddHeaderMarkup = ""
  evenHeaderMarkup = ""
  oddFooterMarkup = ""
  evenFooterMarkup = ""
}
\\new Staff <<
"""
    formats = ["\\voiceOne", "\\voiceTwo", "\\voiceThree", "\\voiceFour"]
    format_iter = 0
    viter = 0
    for voice in voices:
        ly_output += "  \\new Voice = \"" + str(viter) + "\"" + linebr
        ly_output += "    { " + formats[format_iter] + " "
        ly_output += "\\time " + time_signature + " "
        ly_output += voice + "}" + linebr

        viter += 1
        if format_iter < 3:
            format_iter += 1
    ly_output += ">>"

    return ly_output


""" helper function to generate png from ly file

"""


def _generatePng(temp_dir):
    lpdir = "lilypond"
    filepath = str(os.path.join(temp_dir, "file.ly"))
    pngpath = str(os.path.join(temp_dir, "preview"))
    subprocess.run(
        lpdir + " -fpng -dresolution=300 -dpreview -o " + pngpath + "/ " + filepath,
        # lpdir + " -dbackend=eps -dresolution=600 --png -o " + pngpath + "/ " + filepath,
        shell=True,
        capture_output=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


def displayNotes(voices, time_signature):
    """Return an image of the score

    :param voices: List of voices, where each voice is a string in lilypond formatting
    :type voices: list
    :param time_signature: the time signature
    :type time_signature: string
    :return: Image of the source
    :rtype: IPython.display.image
    """ """"""
    temp_top = os.path.join(os.getcwd(), "")
    temp_dir = tempfile.mkdtemp(dir=temp_top)
    ly_output = _FileGenerator(voices, time_signature)
    with open(os.path.join(temp_dir, 'file.ly'), 'w') as f:
        f.write(ly_output)
    _generatePng(temp_dir)
    pngpath = str(os.path.join(temp_dir, "preview"))
    img = Image(filename=pngpath + '.png')
    shutil.rmtree(temp_dir)

    return img


def convertNotes(voices):
    """Return lists of keys, frequencies and durations from voices

    :param voices: List of voices, where each voice is a string in lilypond formatting
    :type voices: list
    :return: List of keys, frequencies and durations
    :rtype: (list, list, list)
    """ """"""
    allkeys = []
    allfreqs = []
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
            for i in range(1, len(note), 2):
                if i + 1 < len(note):
                    if note[i : i + 2] == "is":
                        sharp += 1
                    elif note[i : i + 2] == "es":
                        sharp -= 1

            key = notelst.index(note[0]) + 12 * op.countOf(rest, "'") - 12 * op.countOf(rest, ",") + sharp

            keys.append(key)
            freq = (261.63 / 2.0) * np.power(2, key / 12.0)
            freqs.append(freq)

            i = len(note) - 1

            lmult = 1

            add = 0.5

            while note[i] == ".":
                lmult += add
                add *= 0.5
                i -= 1

            base_duration = ""

            nums = "0123456789"

            while note[i] in nums:
                base_duration = note[i] + base_duration
                i -= 1

            dur = 1.0
            if len(base_duration) > 0:
                dur = 4.0 / int(base_duration)

            durations.append(dur * lmult)

        allkeys.append(keys)
        allfreqs.append(freqs)
        alldurations.append(durations)
    return allkeys, allfreqs, alldurations


@deprecation.deprecated(details="Use the midi output to play notes instead", deprecated_in="0.0.0")
def playNotes(voice_frequencies):
    """Plays the notes with the given frequencies, and returns

    :param voice_frequencies: List of frequencies to play
    :type voice_frequencies: list
    :return: sound array played, sound array of the last voice
    :rtype: tuple
    """
    maxdur = 0
    for frequencies in voice_frequencies:
        if len(frequencies) > maxdur:
            maxdur = len(frequencies)
    sample_rate = 44100  # sampling rate, Hz, must be integer

    quarter_len = int(sample_rate / 3.0)

    sample_len = quarter_len * maxdur
    sample_sum = np.zeros(sample_len)
    times = np.arange(quarter_len) / sample_rate

    for frequencies in voice_frequencies:
        cur_time = 0
        for freq in frequencies:
            # print(freq)
            sample = (np.sin(2 * np.pi * times * freq)).astype(np.float32)

            # adding overtones to reduce earache from
            # hearing pure tones
            for k in [0.5, 1, 2]:
                prefac = 0
                if k == 0.5:
                    prefac = 0.15
                if k == 1:
                    prefac = 0.5
                if k == 2:
                    prefac = 0.15

                for i in range(1, 8):
                    sample += prefac * (np.sin(k * i * 2 * np.pi * times * freq)).astype(np.float32) / np.power(1.3, i)

            for i in range(0, len(sample)):
                sample_sum[quarter_len * cur_time + i] += sample[i]
            cur_time += 1

    sample_sum = sample_sum.astype(np.float32)

    output_bytes = (sample_sum / np.max(np.abs(sample_sum))).tobytes()

    _playBytes(output_bytes, sample_rate)

    return sample_sum, sample


"""Plays notes from bytes

Parameters
----------
output_bytes : np.array
    bytes to play
sample_rate:
    sample rate

"""


def _playBytes(output_bytes, sample_rate):
    if config.play_audio:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)

        stream.write(output_bytes)

        stream.stop_stream()
        stream.close()

        p.terminate()


"""Gets the representation of duration as a lilypond string

Parameters
----------
n : int
    duration integer

Returns
-------
string
    duration string

"""


def _getDurationRepresentation(n):
    if n not in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128]:
        raise Exception("unsupported note length")
    if n == 3:
        return "4."
    if n == 6:
        return "8."
    if n == 12:
        return "16."
    if n == 24:
        return "32."
    if n == 48:
        return "64."
    if n == 96:
        return "128."
    return str(n)


class Piece:
    """Piece that can be played and displayed"""

    def __init__(self, tempo, time_signature="4/4"):
        self.tempo = tempo
        self.time_signature = time_signature

        self.instruments = []
        self.voices = []
        self.live_voices = []

        self.score_object = Ipyscore()

    def getScoreObject(self):
        """Gets an editable object of the score

        :return: an object with a widget for the score and text entry to change notes
        :rtype: widgets.VBox
        """
        box = [self.score_object]
        for v in self.live_voices:
            box.append(v)
        return widgets.VBox(box)

    def _setScore(self):
        keys, durations = getVexVoices([lv.value for lv in self.live_voices])
        self.score_object.nkeys = keys
        self.score_object.durations = durations

    def _updateScore(self, change):
        try:
            keys, durations = getVexVoices([lv.value for lv in self.live_voices])
            self.score_object.nkeys = keys
            self.score_object.durations = durations
            self.voices = [lv.value for lv in self.live_voices]
            self._setMidi()
        except:
            donothing = True

    """adds a voice
    
    """

    def addVoice(self, voice, nl=None, instrument=1):
        """_summary_

        :param voice: lilypond style string for a given voice
        :type voice: string
        :param nl: default length, if any, defaults to None
        :type nl: int, optional
        :param instrument: midi code for instrument for the given voice, defaults to 1 (piano)
        :type instrument: int, optional
        """
        if nl is None:
            voice_arr = voice.split(" ")
            for i in range(0, len(voice_arr)):
                if voice_arr[i][-1] not in "123456789.":
                    voice_arr[i] += "4 "
                else:
                    voice_arr[i] += " "

            result = "".join(voice_arr)
            self.voices.append(result)
            ind = len(self.voices)
            w = widgets.Textarea(
                description="Voice " + str(ind),
                continuous_update=True,
                value=result,
                style={"background": "#F9F9FF", "description_width": "100px", "font_size": "20pt"},
                layout=Layout(min_height="50px", min_width="800px"),
            )
            w.observe(self._updateScore)
            self.live_voices.append(w)
        else:
            self._addVoiceNL(voice, nl)

        self.instruments.append(instrument)

        self._setMidi()
        self._setScore()

    def _addVoiceNL(self, voice, notelengths):
        result = ""
        if not (isinstance(type(notelengths), type([1]))):
            voice_arr = voice.split(" ")
            for note in voice_arr:
                result += note + _getDurationRepresentation(notelengths) + " "
        else:
            voice_arr = voice.split(" ")
            if not len(voice_arr) == len(notelengths):
                raise Exception("number of notes does not match number of durations")
            for i in range(0, len(voice_arr)):
                result += voice_arr[i] + _getDurationRepresentation(notelengths[i]) + " "

        self.voices.append(result)

        ind = len(self.voices)
        w = widgets.Textarea(
            description="Voice " + str(ind),
            continuous_update=True,
            value=result,
            style={"background": "#F9F9FF", "description_width": "100px", "font_size": "20pt"},
            layout=Layout(min_height="50px", min_width="800px"),
        )
        w.observe(self._updateScore)
        self.live_voices.append(w)

    def getScore(self):
        """Returns an image of the score

        :return: image of the score
        :rtype: Ipython.display.Image
        """
        img = displayNotes(self.voices, self.time_signature)
        return img

    def _setMidi(self):
        keys, freas, durs = convertNotes(self.voices)

        self.midi = MIDIFile(len(keys))

        for voice_ind in range(0, len(keys)):
            voice = keys[voice_ind]
            voice_durs = durs[voice_ind]
            t = 0.0
            self.midi.addTempo(voice, t, self.tempo)
            for i in range(0, len(voice)):
                note = voice[i]
                notelen = voice_durs[i]
                self.midi.addProgramChange(voice_ind, 0, t, self.instruments[voice_ind])
                self.midi.addNote(voice_ind, 0, 48 + note, t, notelen, 80)
                t += notelen

    def play(self):
        """plays the midi file for the piece"""
        with open("./music_file.mid", "wb") as output_file:
            self.midi.writeFile(output_file)

        pygame.init()
        pygame.mixer.music.load("./music_file.mid")
        pygame.mixer.music.play()

    def stop(self):
        """stops the playing of the piece's midi file"""
        pygame.mixer.music.stop()
