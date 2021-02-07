"""VideoAtRNP Crawler

Author: Pedro Vinicius Almeida de Freitas

Created in: 10/01/2021

This tool uses the VideoAtRNP API to search for all videos in the platform and
download them. The user can select any number of videos to download from the platform.
The VideoAtRNP site is mainly a educational videos hosting platform.

This tool requires `requests` to be installed within the Python
environment you are running this tool in.

This file can also be imported as a module and contains the following
functions:

    * sizeof_fmt - Formats number of bytes to a human readable string.
    * scandown - Scan and print a xml tree.
    * log - Rudimentary logging function.
    * download_file - Downloads a file from the provided url.
    * crawl_and_download - Crawls the VideoAtRNP API, collecting and downloading video data.
"""

import requests
import os
import sys
from xml.dom import minidom
import time
import datetime
import argparse

# Please put your client key here
CLIENT_KEY = None


def sizeof_fmt(n_bytes: int, suffix: str = 'B'):
    """Formats number of bytes to a human readable string.
    Function by: Fred Cirera and Wai Ha Lee
    Sources:
    https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size

    :param n_bytes: Number of bytes to format.
    :type n_bytes: int, optional

    :param suffix: Suffix to put after each Unit (e.g. B: KiB, MiB, ...)
    :type suffix: str, optional

    :returns: A string with human readable representation of a set amount of bits.
    :rtype: str
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(n_bytes) < 1024.0:
            return "%3.1f %s%s" % (n_bytes, unit, suffix)
        n_bytes /= 1024.0
    return "%.1f %s%s" % (n_bytes, 'Yi', suffix)


def scandown(elements, indent=0):
    """Scan and print a xml tree.

    :param elements: a Xml.dom node or a list of nodes.

    :param indent: How much to ident in each branch.
    :type indent: int, optional

    :returns: It just prints all nodes.
    """
    if not isinstance(elements, list) and elements:
        log("   " * indent + "nodeName: " + str(elements.nodeName))
        log("   " * indent + "nodeValue: " + str(elements.nodeValue))
        log("   " * indent + "childNodes: " + str(elements.childNodes))
        scandown(elements.childNodes, indent + 1)
    else:
        for el in elements:
            log("   " * indent + "nodeName: " + str(el.nodeName))
            log("   " * indent + "nodeValue: " + str(el.nodeValue))
            log("   " * indent + "childNodes: " + str(el.childNodes))
            scandown(el.childNodes, indent + 1)


def log(string: str, file=None):
    """Rudimentary logging function.

     :param string: What string to log.
     :type string: str, optional

     :param file: Reference to a open file where to write.

     :returns: It just prints or writes the string to a file.
     """
    print(string)
    if file:
        file.write(string + '\n')


def download_file(url: str, save_dir: str, local_filename: str = None, verbose: bool = True):
    """Downloads a file from the provided url.

    :param url: Url for the file.
    :type url: str, optional

    :param save_dir: Path to where the file will be saved.
    :type save_dir: str, optional

    :param local_filename: Local equivalent to the file referenced in the url, the function will try to redowload the file if it has less than 150 bytes.
    :type local_filename: str, optional

    :param verbose: Boolean to toggle wether or not to print additional content.
    :type verbose: bool, optional

    :returns: The size in bytes of the downloaded content, if it failed, size will be zero.
    :rtype: int
    """

    if not local_filename:
        local_filename = url.split('/')[-1]
    localFilePath = save_dir + '/' + local_filename
    if os.path.exists(localFilePath):
        file_size = os.path.getsize(localFilePath)
        if file_size >= 150:
            print("Already downloaded, skipping!")
            return file_size
    with open(localFilePath, 'wb') as f:
        start = time.clock()
        try:
            r = requests.get(url, stream=True)
        except Exception as e:
            print(e)
            return 0
        total_length = int(r.headers.get('content-length'))
        dl = 0
        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            # Download in chunks
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                if verbose:
                    done = int(50 * dl / total_length)
                    speed_bytes = dl // (time.clock() - start)
                    sys.stdout.write("\r[%s%s], Speed: %s Mbps, Total: %s" % (
                        '=' * done, ' ' * (50 - done), sizeof_fmt(speed_bytes), sizeof_fmt(total_length)))
                    sys.stdout.flush()
        return int(r.headers.get('content-length'))


def crawl_and_download(client_key: str, save_dir: str, start_id: int = None, start_index: int = 0, max_n: int = 10,
                       log_file_path=None):
    """Crawls the Video@RNP API, collecting and downloading video data.

    :param client_key: The client key provided by the API Admin (Video@RNP).
    :type client_key: str

    :param save_dir: Path to where the file will be saved.
    :type save_dir: str

    :param start_id: The Downloader will start the downloads from this video id.
    :type start_id: str, optional

    :param start_index: The Downloader will start the downloads from a said number of videos
    :type start_index: str, optional

    :param max_n: Max number of videos to download.
    :type max_n: int, optional

    :param log_file_path: Path to save the logs. Optional. e.g. "./"
    :type log_file_path: int, optional

    :returns: None, It automatically saves the videos to the save save_dir.
    :rtype: None
    """
    # Creating the save save_dir
    if not os.path.exists(save_dir):
        print("Save dir not found, creating save dir in:", save_dir)
        os.makedirs(save_dir)

    # Defining the requests user agent and headers
    PARAMS = {'limit': max_n}  # {'address': location}
    HEADERS = {
        "clientkey": client_key}
    # 'User-agent': 'Mozilla/5.0'

    # Requesting the main video xml
    r = requests.get('https://video.rnp.br/services/video',
                     params=PARAMS, headers=HEADERS, timeout=5000000)
    xml = minidom.parseString(r.text)

    # log('### RESULT: ', r.status_code, r.reason)
    # with open("videos.txt","w") as f:
    #   f.write(r.text)
    #   f.close() #to change file access modes
    PARAMS = {}
    SAVE_DIR = save_dir
    LOG_NAME = 'probing.log'
    videos_tag = xml.childNodes[0]
    videos_nodes = videos_tag.childNodes
    total_size = 0
    failed_requests = 0
    denied_requests = 0
    successful_requests = 0

    if log_file_path:
        with open(os.path.join(log_file_path, LOG_NAME), 'a+') as log_file:
            log(f'Starting run for probing {len(videos_nodes)} videos! At {datetime.datetime.now()}', log_file)
    else:
        log(f'Starting run for probing {len(videos_nodes)} videos! At {datetime.datetime.now()}')

    for i, video_node in enumerate(videos_nodes):
        if log_file_path:
            log_file = open(os.path.join(log_file_path, LOG_NAME), 'a+')
        else:
            log_file = None
        video_id = video_node.childNodes[0].childNodes[0].nodeValue
        if i < start_index:
            # print(f'Jumping index {i} until {start_index}.')
            continue
        if start_id is not None:
            if str(start_id) != str(video_id):
                continue
            else:
                print(f' Found id to start from, {start_id} == {video_id}, starting downloads.')
                start_id = None  # if we already passed our starting point, then we dont need to test forom now on

        if (i % 10 == 0) and (i != 0):
            log(f'{failed_requests}/{len(videos_nodes)} failed until now.', log_file)
            log(f'{denied_requests}/{len(videos_nodes)} denied until now.', log_file)
            log(f'{successful_requests}/{len(videos_nodes)} successful until now.', log_file)

        time.sleep(50)
        # if len(glob.glob(SAVE_DIR +'/'+video_id+'*')) > 0:
        #     log('Already downloaded!')
        #     continue
        try:
            r = requests.get(f'https://video.rnp.br/services/video/versions/{video_id}',
                             params=PARAMS, headers=HEADERS)
        except Exception as e:
            print(e)
            continue
        if r.status_code != 200:
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, error in request: {r.status_code} {r.reason}.',
                log_file)
            failed_requests += 1
            continue

        xml = minidom.parseString(r.text)
        versions = xml.childNodes[0]
        best_version = versions.childNodes[0]
        # scandown(best_version.childNodes)

        try:
            url = best_version.getElementsByTagName('url')[0].childNodes[0].nodeValue
            # log(url)
        except Exception as e:
            # log('Error: ', e)
            log(best_version, log_file)
            log(best_version.getElementsByTagName('url'), log_file)
            log(f'ERROR! Video id:{video_id}, index: {i}', log_file)
            continue
        video_format = best_version.getElementsByTagName('fileFormat')[0].childNodes[0].nodeValue
        video_download_name = video_id + '.' + video_format.lower()
        # log(video_download_name)
        # r = requests.get(url, stream=True)
        # video_size = int(r.headers.get('content-length'))
        video_size = download_file(url, SAVE_DIR, local_filename=video_download_name, verbose=False)

        if video_size == 0:
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, failed to download file. (Probably too many requests)',
                log_file)
            denied_requests += 1
        else:
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, request successful with size {sizeof_fmt(video_size)}',
                log_file)
        total_size += video_size
        successful_requests += 1

    if log_file_path and not log_file:
        log_file = open(os.path.join(log_file_path, LOG_NAME), 'a+')

    log(f'Total size: {total_size}', log_file)
    log(f'Total size: {sizeof_fmt(total_size)}', log_file)
    log(f'Number of successful requests:{successful_requests}', log_file)
    log(f'Number of denied requests:{denied_requests}', log_file)
    log(f'Number of failed requests:{failed_requests}', log_file)

    if log_file:
        log_file.close()


if __name__ == "__main__":
    # Defining the script's arguments
    parser = argparse.ArgumentParser()
    # Video 20827/31366, Id:23097, error in request: 404 Not Found.
    parser.add_argument("save_dir", type=str,
                        help="The path to the save_dir in which to save the downloads", default='./rnp_downloads/')
    parser.add_argument("--key", type=str,
                        help="Your Video@RNP API access key. You can also provide it by putting it in the start of this script.", default=None)
    parser.add_argument("--start_id", type=str,
                        help="The Downloader will start the downloads from this video id", default=None)
    parser.add_argument("--limit", type=int,
                        help="Limit of videos to download", default=1000000)
    parser.add_argument("--start_index",
                        help="The Downloader will start the downloads from a said number of videos", type=int,
                        default=0)
    parser.add_argument("--log_path", type=str,
                        help="Path to save the logs. e.g. './'", default=None)
    args = parser.parse_args()

    key = None
    if CLIENT_KEY:
        key = CLIENT_KEY
    elif args.key:
        key = args.key
    else:
        quit('Please provide your API key either via arguments or in the start of this script.')

    crawl_and_download(client_key=key, save_dir=args.save_dir, start_id=args.start_id, start_index=args.start_index, max_n=args.limit, log_file_path=args.log_path)
