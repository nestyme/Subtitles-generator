import time
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa
import argparse
import os
from glob import glob

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-video', type=str,
                        help='path to audiofile')
    arguments = parser.parse_args()
    return arguments

def recognize(wav_filename):
    data, s = librosa.load(wav_filename)
    librosa.output.write_wav('tmp.wav', data, s)
    y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    wavfile.write('tmp_32.wav', s, y)

    r = sr.Recognizer()
    with sr.AudioFile('tmp_32.wav') as source:
        audio = r.record(source)  

    print('audiofile loaded')

    try:
        result = r.recognize_google(audio, language = 'ru').lower()
    except sr.UnknownValueError:
        print("cannot understand audio")
        result = ''
        os.remove(wav_filename)  
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(' {}'.format(result))
   #  return result

def get_audio(video):
    os.system('ffmpeg -y  -threads 4\
 -i {} -f wav -ab 192000 -vn {}'.format(video, 'current.wav'))

def split_into_frames(audiofile):
    data, sr = librosa.load(audiofile)
    duration = librosa.get_duration(data, sr)
    print('video duration, hours: {}'.format(duration/3600))
    for i in range(0,int(duration-1),50):
        tmp_batch = data[(i)*sr:sr*(i+50)]
        librosa.output.write_wav('samples/{}.wav'.format(chr(int(i/50)+65)), tmp_batch, sr)

if __name__ == '__main__':
    start = time.time()
    args = get_arguments()
    get_audio(args.video)
    split_into_frames('current.wav')
    files = sorted(glob('samples/*.wav'))
    print(files)
    open('result.txt', 'w', encoding = 'utf-8').write('')
    for file in files:
        print(file)   
        recognize(file)
    end = time.time()
    print('elapsed time: {}'.format(end - start))
    os.system('rm samples/*')
