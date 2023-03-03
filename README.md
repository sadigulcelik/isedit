# Interactive Score Editor
A python library that combines score editing tools with audio output.<br>
![image](https://img.shields.io/badge/license-Apache--2.0-brightgreen)
![image](https://img.shields.io/github/issues/sadigulcelik/interactive-score-editor)

## Overview

Interactive Score Editor is a python library that helps bridge a music notation library (such as Lilypond via Abjad(https://abjad.github.io/index.html) to an audio player (such as pydub). The goal is to resolve the following: "Abjad provides no audio output beyond LilyPond’s built-in MIDI functionality" (https://abjad.github.io/first_steps/audience.html). Using LilyPond's MIDI is will take longer and be more complicated than a built in feature to play notes directly.

A successful implementation will be helpful both for individuals creating music-composition tools / applications, as well as individuals looking to play around with music composition and sound in a notebook, and will cut the time from starting a music project to hearing actual sound (an element which has been a personal annoyance).
