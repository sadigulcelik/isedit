from src import *


def test_FileGenerator():
    voices = ["c' d' e' f' g' a' b' c''", "e'"]
    result = FileGenerator(voices)

    def getNextVoice(voicestring):
        start = voicestring.find("{")
        end = voicestring.find("}")
        voice = voicestring[start + 1 : end].split(" ")
        voicearr = [a for a in voice if len(a) > 0]
        assert "{" not in voice
        assert "}" not in voice
        return voicearr, voicestring[end + 1 :]

    voice1, remaining1 = getNextVoice(result)
    voice2, remaining2 = getNextVoice(remaining1)

    # we test that when we parse, we get what we expect

    assert np.array_equal(voice1, ["\\voiceOne", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"])
    assert np.array_equal(voice2, ["\\voiceTwo", "e'"])


def test_generatePng():
    with open("file.ly", "w") as f:
        f.write(
            """\\version "2.24.1" 
        \\new Staff <<
    \\new Voice = "0" { \\voiceOne c' d' e' f' g'}
    >>"""
        )
    generatePng("")

    # we test that the sheet music image is generated
    assert os.path.isfile("preview.png")

    os.remove("file.ly")
    os.remove("preview.png")
    if(os.path.exists("preview.preview.png")):
        os.remove("preview.preview.png")


def test_displayNotes():
    # we test that an image is returned
    img = displayNotes(["c' d' e' f' g'"])
    assert type(img) == Image


def test_convertNotes():
    # check notes are correctly translated into integers
    assert np.array_equal(
        np.array(convertNotes(["c a'", "c'"])[0], dtype=object),
        np.array([[0, 21], [12]], dtype=object),
    )

    result = convertNotes(["c a'", "c'"])[1]

    # ensure roughly 440 tuning in frequency transformation
    assert np.linalg.norm(result[0][0] - 130.82) < 1
    assert np.linalg.norm(result[0][1] - 440.01) < 1
    assert np.linalg.norm(result[1][0] - 261.63) < 1


def test_playNotes():
    keys = [[12, 14, 16]]
    freqs = [[261.63, 293.66974569918125, 329.63314428399565]]
    piece, lastnote = playNotes(freqs)

    correct_values = {
        0: 0.0,
        5000: -1.0940858,
        10000: 0.97059435,
        15000: -0.118024155,
        20000: 1.0746915,
        25000: -0.4021347,
        30000: -0.011225048,
        35000: -1.5115523,
        40000: 1.273912,
    }
    # we assert that the piece is as expected by checking some values
    for i in range(0, 44100, 5000):
        assert np.linalg.norm(piece[i] - correct_values[i]) <= 0.05
