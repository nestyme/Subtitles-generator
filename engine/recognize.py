import time
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa
import argparse
import os
from glob import glob
from logmmse import logmmse_from_file
from engine.process_rus import reformat_rus

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-video', type=str,
                        help='path to audiofile')
    arguments = parser.parse_args()
    return arguments

def simple_punctuation(text):
    try:
        result = text[0].upper()
        for char in text[1:]:
            if char.isupper():
                result += '.' + char
            else:
                result += char
        result = result.replace(' .', '. ')
        # block od simple russian lang euristics:
        return reformat_rus(result+'.')
    except:
        return text

def recognize(wav_filename):
    data, s = librosa.load(wav_filename)
    librosa.output.write_wav('tmp.wav', data, s)
    y = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
    wavfile.write('tmp_32.wav', s, y)
    r = sr.Recognizer()
    with sr.AudioFile('tmp_32.wav') as source:
        audio = r.record(source)

    print('audiofile loaded')

    try:
        result = r.recognize_google(audio, language='ru')
    except sr.UnknownValueError:
        print("cannot understand audio")
        result = ''
        os.remove(wav_filename)
    with open('engine/result.txt', 'a', encoding='utf-8') as f:
        f.write(' {}'.format(simple_punctuation(result).replace('..','.')))


#  return result

def get_audio(video):
    os.system('ffmpeg -y  -threads 4\
 -i {} -f wav -ab 192000 -vn {}'.format(video, 'current.wav'))


def split_into_frames(audiofile):
    data, sr = librosa.load(audiofile)
    duration = librosa.get_duration(data, sr)
    print('video duration, hours: {}'.format(duration / 3600))
    for i in range(0, int(duration - 1), 150):
        tmp_batch = data[(i) * sr:sr * (i + 150)]
        librosa.output.write_wav('engine/samples/{}.wav'.format(chr(int(i / 150) + 165)), tmp_batch, sr)


def video2text(video):
    start = time.time()
    get_audio(video)
    split_into_frames('current.wav')
    files = sorted(glob('engine/samples/*.wav'))
    print(files)
    open('result.txt', 'w', encoding='utf-8').write('')
    for file in files:
        print(file)
        recognize(file)
    end = time.time()
    print('elapsed time: {}'.format(end - start))
    os.system('rm engine/samples/*')
    os.system('rm engine/tmp*')


if __name__ == '__main__':
    args = get_arguments()
    video2text(args.video)
