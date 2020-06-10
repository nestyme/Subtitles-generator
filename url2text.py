import argparse
import os
from engine.download_video import download_video
from engine.recognize import video2text
from engine.process_rus import reformat_rus

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', type=str,
                        help='path to audiofile')
    arguments = parser.parse_args()
    return arguments


def simple_punctuation(text):
    result = text[0].upper()
    for char in text[1:]:
        if char.isupper():
            result += '.' + char
        else:
            result += char
    result = result.replace(' .', '. ')
    # block od simple russian lang euristics:
    return reformat_rus(result[1:]+'.')


def recognize(url):
    download_video('engine/tmp', url)
    print('video uploaded on server')
    video2text('engine/tmp*')
    print('video recognized')
    text = open('engine/result.txt', 'r', encoding='utf-8').read()
    return simple_punctuation(text)


def url2text(url):
    # TODO: rewrite with no system calls
    os.system('rm tmp*')
    os.system('engine/tmp*')
    os.system('rm engine/current.wav')

    with open('engine/result.txt', 'w', encoding='utf-8') as f:
        f.write('')
    text = recognize(url)
    os.system('rm engine/result.txt')
    print(text)
    return text
    os.system('rm current.wav')
    os.system('rm tmp*')


if __name__ == '__main__':
    args = get_arguments()
    url2text(args.url)
