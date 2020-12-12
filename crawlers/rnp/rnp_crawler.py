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
    '''Formats number of bytes to a human readable unity.

    :param n_bytes: Number of bytes to format.
    :type n_bytes: int, optional

    :param suffix: Suffix to put after each Unit (e.g. B: KiB, MiB, ...)
    :type suffix: str, optional

    :returns: A string with human readable representation of a set amount of bits.
    :rtype: str
    '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(n_bytes) < 1024.0:
            return "%3.1f%s%s" % (n_bytes, unit, suffix)
        n_bytes /= 1024.0
    return "%.1f%s%s" % (n_bytes, 'Yi', suffix)


def downloadFile(url: str, save_dir: str, local_filename: str = None, verbose: bool = True):
    '''Downloads a file from the provided url.

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
    '''

    if not local_filename:
        local_filename = url.split('/')[-1]
    localFilePath = save_dir + '/' + local_filename
    if os.path.exists(localFilePath):
        file_size = os.path.getsize(localFilePath)
        if file_size <= 150:
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


def scandown(elements, indent):
    '''Scan and print a xml tree

    :param elements: Xml.dom nodes.

    :param indent: How much to ident in each branch.
    :type indent: int, optional

    :returns: It just prints all nodes.
    '''

    for el in elements:
        log("   " * indent + "nodeName: " + str(el.nodeName))
        log("   " * indent + "nodeValue: " + str(el.nodeValue))
        log("   " * indent + "childNodes: " + str(el.childNodes))
        scandown(el.childNodes, indent + 1)


def log(string: str, file=None):
    '''Rudimentary logging function.

     :param string: What string to log.
     :type string: str, optional

     :param file: Reference to a open file where to write.

     :returns: It just prints or writes the string to a file.
     '''
    print(string)
    if file:
        file.write(string + '\n')


def crawl_and_download(client_key: str, start_id: int, start_index: int, max_n: int, save_dir: str):
    '''Crawls the Video@RNP API, collecting and downloading video data.

    :param client_key: The client key provided by the API Admin (Video@RNP).
    :type client_key: str, optional

    :param start_id: The Downloader will start the downloads from this video id.
    :type start_id: str, optional

    :param start_index: The Downloader will start the downloads from a said number of videos
    :type start_index: str, optional

    :param max_n: Max number of videos to download.
    :type max_n: int, optional

    :param save_dir: Path to where the file will be saved.
    :type save_dir: str, optional

    :returns: None, It automatically saves the videos to the save save_dir.
    :rtype: None
    '''

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
    videos_tag = xml.childNodes[0]
    videos_nodes = videos_tag.childNodes
    total_size = 0
    failed_requests = 0
    denied_requests = 0
    successful_requests = 0

    with open('probing.log', 'a+') as file:
        log(f'Starting run for probing {len(videos_nodes)} videos! At {datetime.datetime.now()}', file)

    for i, video_node in enumerate(videos_nodes):
        file = open('probing.log', 'a+')
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
            log(f'{failed_requests}/{len(videos_nodes)} failed until now.', file)
            log(f'{denied_requests}/{len(videos_nodes)} denied until now.', file)
            log(f'{successful_requests}/{len(videos_nodes)} successful until now.', file)

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
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, error in request: {r.status_code} {r.reason}.', file)
            failed_requests += 1
            continue

        xml = minidom.parseString(r.text)
        versions = xml.childNodes[0]
        best_version = versions.childNodes[0]
        # scandown(best_version.childNodes,0)
        try:
            url = best_version.getElementsByTagName('url')[0].childNodes[0].nodeValue
            # log(url)
        except Exception as e:
            # log('Error: ', e)
            log(best_version, file)
            log(best_version.getElementsByTagName('url'), file)
            log(f'ERROR! Video id:{video_id}, index: {i}', file)
            continue
        video_format = best_version.getElementsByTagName('fileFormat')[0].childNodes[0].nodeValue
        video_download_name = video_id + '.' + video_format.lower()
        # log(video_download_name)
        # r = requests.get(url, stream=True)
        # video_size = int(r.headers.get('content-length'))
        video_size = downloadFile(url, SAVE_DIR, local_filename=video_download_name, verbose=False)

        if video_size == 0:
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, failed to download file. (Probably too many requests)',
                file)
            denied_requests += 1
        else:
            log(f'Video {i}/{len(videos_nodes)}, Id:{video_id}, request successful with size {sizeof_fmt(video_size)}',
                file)
        total_size += video_size
        successful_requests += 1
        file.close()

    with open('probing.log', 'a+') as file:
        log(f'Total size: {total_size}', file)
        log(f'Total size: {sizeof_fmt(total_size)}', file)
        log(f'Number of successful requests:{successful_requests}', file)
        log(f'Number of denied requests:{denied_requests}', file)
        log(f'Number of failed requests:{failed_requests}', file)


if __name__ == "__main__":
    # Defining the script's arguments
    parser = argparse.ArgumentParser()
    # Video 20827/31366, Id:23097, error in request: 404 Not Found.
    parser.add_argument("start_id", type=str,
                        help="The Downloader will start the downloads from this video id", default=None)
    parser.add_argument("limit", type=int,
                        help="Limit of videos to download", default=10000000)
    parser.add_argument("start_index",
                        help="The Downloader will start the downloads from a said number of videos", type=int,
                        default=0)
    parser.add_argument("save_dir", type=str,
                        help="The path to the save_dir in which to save the downloads", default='./rnp_downloads/')
    args = parser.parse_args()

    crawl_and_download(CLIENT_KEY, args.start_id, args.limit, args.start_index, args.save_dir)