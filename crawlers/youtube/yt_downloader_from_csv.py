"""Youtube downloader from csv

Author: Pedro Vinicius Almeida de Freitas

Created in: 05/01/2021

This tool takes a Comma Separated Values file with youtube videos URLS as input
and downloads them to the specified directory. It avoids downloading videos that
are already in the destination folder.

This tool requires `youtube_dl` to be installed within the Python
environment you are running this tool in.

This file can also be imported as a module and contains the following
functions:

    * already_downloaded - Tests if the video was already downloaded.
    * download - Downloads a video from a URL.
    * read_csv_and_download_videos - Collects URLs from a csv file and downloads them.
"""

import os
import youtube_dl
import argparse
#from multiprocessing import Pool
from time import sleep


# https://www.youtube.com/watch?v=sQ3aeclQ3QA
# /media/pedropva/datasets/yt_videos/sQ3aeclQ3QA.mp4
def already_downloaded(url: str, save_dir: str):
    """Checks (from the url) if a video was already downloaded in the save save_dir.

    :param url: Youtube Url for the video.
    :type url: str, optional

    :param save_dir: Path to where the videos are saved.
    :type save_dir: str, optional

    :returns: A boolean, True if the video already exists in the save dir, False otherwise.
    :rtype: bool
    """
    video_id = url.split('v=')[-1]
    video_path = save_dir + video_id
    if os.path.isfile(video_path + '.mp4') or os.path.isfile(video_path + '.webm'):
        return True
    else:
        return False


def download(url: str, save_dir: str):
    """Downloads a video from the provided url.

    :param url: Youtube Url for the video.
    :type url: str, optional

    :param save_dir: Path to where the videos are saved.
    :type save_dir: str, optional

    :returns: A boolean, True if the it had success downloading the video, False otherwise.
    :rtype: bool
    """
    try:
        options = {
            # 'verbose': True,
            'format': 'best',
            'outtmpl': save_dir + '%(id)s.%(ext)s',
            # "source_address": "10.0.0.4",
            # 'verbose':False,
            # 'progress_hooks': [my_hook],
            # 'noplaylist' : True,
            # 'postprocessors': [{
            #    'key': 'FFmpegExtractAudio',
            #    'preferredcodec': 'mp3',
            # }],
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            # result = ydl.download([url])
            result = ydl.extract_info(url, download=True)

        filepath = save_dir + result['display_id'] + '.' + result['ext']
        print('downloaded: ', filepath)
        return True
    except Exception as e:
        print(e)
        return False


def read_csv_and_download_videos(csv_path: str, save_dir: str, wait_time: int = 30):
    """Downloads a video from a csv containing youtube urls. One url per line.

    :param csv_path: Path to the csv file with the urls to youtube.
    :type csv_path: str, optional

    :param save_dir: Path to where the videos are saved.
    :type save_dir: str, optional

    :param wait_time: Wait time between requests, use it to not get blocked for too many requests.
    :type wait_time: int, optional

    :returns: A boolean, True if the it had success downloading the video, False otherwise.
    :rtype: bool
    """

    # Creating the save save_dir
    if not os.path.exists(save_dir):
        print("Save dir not found, creating save dir in:", save_dir)
        os.makedirs(save_dir)

    # Reading the csv file
    raw = open(csv_path).read().split('\n')
    raw = [v.replace(',', '') for v in raw if v != '']
    # raw = raw[:5500]

    urls_to_download = [url for url in raw if not already_downloaded(url, save_dir)]
    print(f"{len(raw) - len(urls_to_download)} Videos already downloaded!")

    # try to download all urls until many consecutive fails or done dowloading all.
    while (len(urls_to_download) > 0):
        fails_sequence = 0
        failed_urls = []
        # Uncomment this part and comment the 'for' for multi threading
        # p = Pool(32)
        # p.starmap(download, zip(urls_to_download))

        # Try to download each video
        for url in urls_to_download:
            print('Downloading from url:', url)
            result = download(url, save_dir)
            if not result:
                print('### Failed downloading video! ###')
                fails_sequence += 1
                failed_urls.append(url)
            else:
                fails_sequence = 0

                sleep(30)

            if (fails_sequence > 100):  # if we failed more than N times, then just give up and try next time
                break

        urls_to_download = failed_urls
        print(f'There are {len(raw) - len(urls_to_download)} out of {len(raw)} videos downloaded!')

        sleep(wait_time)


if __name__ == "__main__":
    # Defining the script's arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str,
                        help="Path to the csv file containing a youtube url per line")
    parser.add_argument("save_dir", type=str,
                        help="The path to the save_dir in which to save the downloads", default='./yt_downloads/')
    parser.add_argument("--wait",
                        help="Time in seconds to wait between downloads (so not to overload youtube)",
                        default=10)

    # Parsing arguments
    args = parser.parse_args()

    read_csv_and_download_videos(args.csv_path, args.save_dir, args.wait)
