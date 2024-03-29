# Interactive Score Editor

A python library that combines score editing tools with audio output.<br>
[![PyPI](https://img.shields.io/pypi/v/isedit)](https://pypi.org/project/isedit/)
[![Build Status](https://github.com/sadigulcelik/isedit/actions/workflows/build.yml/badge.svg)](https://github.com/sadigulcelik/isedit/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/sadigulcelik/isedit/branch/main/graph/badge.svg?token=Y3YYB6AYD1)](https://codecov.io/gh/sadigulcelik/isedit)
![image](https://img.shields.io/badge/license-Apache--2.0-brightgreen)
![image](https://img.shields.io/github/issues/sadigulcelik/isedit)
[![docs](https://img.shields.io/badge/docs-is%20edit-blue)](https://sadigulcelik.github.io/isedit/)

## Overview

Interactive Score Editor is a python library that helps bridge a music notation library (such as Lilypond via Abjad(https://abjad.github.io/index.html) to an audio player (such as pydub). The goal is to resolve the following: "Abjad provides no audio output beyond LilyPond’s built-in MIDI functionality" (https://abjad.github.io/first_steps/audience.html).

A successful implementation will be helpful both for individuals creating music-composition tools / applications, as well as individuals looking to play around with music composition and sound in a notebook, and will cut the time from starting a music project to hearing actual sound (an element which has been a personal annoyance).

# Installation

Prerequisites:

- Python >=3.7,
- lilypond, portaudio
- numpy, pyaudio, midiutil, ipython, pygame

To install python packages:

```bash
$ pip install numpy
$ pip install pyaudio
$ pip install midiutil
$ pip install ipython
$ pip install pygame
```

Lilypond (https://lilypond.org) and portaudio (http://www.portaudio.com) can be installed from their websites, with brew

```
$ brew install lilypond
$ brew install portaudio
```

or with apt

```
# sudo apt install portaudio19-dev python3-pyaudio
# sudo apt install -y lilypond
```

Ensure that lilypond runs from the command line by running

```bash
$ lilypond --version
```

# Quick start example

```python
import isedit
Piece = isedit.Piece
p1 = Piece(60, "3/4")

p1.addVoice("e' f' g'", 4)
p1.addVoice("e' f' g'", 4)
p1.addVoice("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4 b'4 c''2.")
p1.play()
p1.getScore()
```

The above example demonstrates the primary functionality of the piece object; the ability to play and display notes using the same object. In the newest release, the experimental `p1.getScoreObject()` option makes editing notes even easier.

# Contributions

See the guidelines for [Contributing](https://github.com/sadigulcelik/isedit/blob/main/CONTRIBUTING.md)
