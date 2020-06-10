from __future__ import unicode_literals
import youtube_dl
import argparse
import time
from google_drive_downloader import GoogleDriveDownloader as gdd



def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', type=str,
                        help='path to audiofile')
    arguments = parser.parse_args()
    return arguments


def download_video(title, url):
    ydl_opts = {'outtmpl': '{}.%(ext)s'.format(title)}
    if 'youtube' in url:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    if 'drive.google' in url:
        if 'mp3' in url or 'wav' in url or 'm4a' in url:
            gdd.download_file_from_google_drive(file_id=url.split('/')[-2], dest_path='engine/tmp.mp3')
        else:
            gdd.download_file_from_google_drive(file_id=url.split('/')[-2], dest_path='engine/tmp.mp4')


if __name__ == '__main__':
    args = get_arguments()
    start = time.time()
    download_video('tmp', args.url)
    end = time.time()
    print('elapsed downloading time: {}'.format(end - start))
