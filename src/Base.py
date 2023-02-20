
import tempfile

import os

import operator as op
from IPython.display import Image

import subprocess
import shutil

import time

import numpy as np
import pyaudio





def FileGenerator(voices):
    
    linebr = """
"""
    ly_output = """\\version "2.24.1"
\\new Staff <<
"""
    formats = ["\\voiceOne","\\voiceTwo","\\voiceThree","\\voiceFour"]
    format_iter = 0  
    viter = 0;
    for voice in voices:
        ly_output+="  \\new Voice = \""+str(viter)+"\""+linebr
        ly_output+="    { "+formats[format_iter]+" "
        ly_output += voice + "}"+linebr
        
        viter +=1
        if(format_iter<3):  
            format_iter+=1
    ly_output += ">>"
    
    return ly_output

def generatePng(temp_dir):
    lpdir = "/Users/sadigulcelik/lilypond/bin/lilypond"
    filepath = str(os.path.join(temp_dir,"file.ly"))
    pngpath = str(os.path.join(temp_dir,"preview"))
    subprocess.run(lpdir+" -fpng -dresolution=300 -dpreview -o "+pngpath +"/ "+filepath,shell = True,
                  capture_output=False,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT
                  )
def displayNotes(voices):
    # temp_top = os.path.join(os.getcwd(),"ise_temp-a8j49")
    # if(os.path.isdir(temp_top)):
    #     shutil.rmtree(temp_top)
    # os.mkdir(temp_top)
    temp_top = os.path.join(os.getcwd(),"temp")
    temp_dir = tempfile.mkdtemp(dir = temp_top)
    ly_output = FileGenerator(voices)
    with open(os.path.join(temp_dir,'file.ly'), 'w') as f:
        f.write(ly_output)
    generatePng(temp_dir)
    pngpath = str(os.path.join(temp_dir,"preview"))
    img = Image(filename=pngpath+'.png') 
    shutil.rmtree(temp_dir)
    
    return img

def convertNotes(voices):
    allkeys = []
    allfreqs = []
    for voice in voices:
        notes = voice.split(" ")
        keys = []
        freqs = []
        notelst = list("c-d-ef-g-a-b")
        for note in notes:
            if(len(note)==0):
                continue
            rest = list(note[1:])
            sharp = 0;
            for i in range(1,len(note),2):
                if(i+1<len(note)):
                    if(note[i:i+2] == "is"):
                        sharp+=1
                    elif(note[i:i+2] == "es"):
                        sharp-=1
                
            
            key = notelst.index(note[0])+ 12*op.countOf(rest,"'") - 12 *op.countOf(rest,",")+sharp
            
            keys.append(key)
            freq = (261.63/2.0)*np.power(2,key/12.0)
            freqs.append(freq)
        allkeys.append(keys)
        allfreqs.append(freqs)
    return allkeys, allfreqs

def playNotes(voice_frequencies):
    maxdur = 0;
    for frequencies in voice_frequencies:
        if(len(frequencies)> maxdur):
            maxdur = len(frequencies)
    sample_rate = 44100  # sampling rate, Hz, must be integer
    
    quarter_len = int(sample_rate/3.0)
    
    sample_len = quarter_len*maxdur
    sample_sum = np.zeros(sample_len)
    times = np.arange(quarter_len)/sample_rate
    
    for frequencies in voice_frequencies:
        cur_time = 0;
        for freq in frequencies:
            # print(freq)
            sample = (np.sin(2 * np.pi * times* freq)).astype(np.float32)
            
            # adding overtones to reduce earache from 
            # hearing pure tones
            for k in [0.5,1,2]:
                prefac = 0
                if(k==0.5):
                    prefac = 0.15
                if(k == 1):
                    prefac = 0.5
                if(k==2):
                    prefac = 0.15

                for i in range(1,8):
                    sample += prefac *(np.sin(k*i*2*np.pi *times*freq)).astype(np.float32)/np.power(1.3,i)

            for i in range(0,len(sample)):
                sample_sum[quarter_len*cur_time+i]+= sample[i]
            cur_time+=1
                
    sample_sum = sample_sum.astype(np.float32)
    
    p = pyaudio.PyAudio()
    
    output_bytes = (sample_sum/np.max(np.abs(sample_sum))).tobytes()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    stream.write(output_bytes)

    stream.stop_stream()
    stream.close()

    p.terminate()
    
    return sample_sum,sample

        
        