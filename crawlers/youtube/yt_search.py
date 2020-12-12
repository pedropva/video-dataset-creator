import os
import youtube_dl
import argparse


def search(query: list, save_dir: str, max_n, wait_time: int = 10):
    '''Performs a query in youtube then downloads every video to the save save_dir.

    :param query: The query strings list, can contain a single string (e.g. ['beach']) or multiple strings (e.g. ['boxing','MMA']).
    :type query: list, optional

    :param save_dir: Path to "save" save_dir (e.g. "./beach_videos/"), where the videos will be stored.
    :type save_dir: str, optional

    :param max_n: Max number of videos to download. It can be a number or simply 'all'
    :type max_n: Any, optional

    :param wait_time: Wait time between requests, use it to not get blocked for too many requests.
    :type wait_time: int, optional

    :returns: None, It automatically saves the videos to the save save_dir.
    :rtype: None
    '''
    with youtube_dl.YoutubeDL(
            {
                "sleep_interval": wait_time,
                # "proxy":'207.91.10.234:8080',
                "quiet": False,
                "verbose": False,
                "no_warnings": True,
                "nooverwrites": True,
                "forceid": True,
                "ignoreerrors": True,
                # "dump_single_json": True,
                'format': 'best',
                "simulate": False,
                "default_search": f"ytsearch{max_n}",
                'outtmpl': save_dir + '%(id)s.%(ext)s',
            }
    ) as ydl:
        # result = ydl.extract_info(query,download=False) # Uncomment this if we just want to extract the info
        ydl.download(query)  # Comment this if you dont want to download the video


def main(query_word: str, save_dir: str, max_n):
    '''Performs a query in youtube then downloads every video to the save save_dir.

    :param query_word: The query string, can only be a single string (e.g. "beach") .
    :type query: str, optional

    :param save_dir: Path to "save" save_dir (e.g. "./beach_videos/"), where the videos will be stored. If any of the directories in the path do not exits then they will be created.
    :type save_dir: str, optional

    :param max_n: Max number of videos to download. It can be a number or simply 'all'
    :type max_n: Any, optional

    :returns: None, It automatically saves the videos to the save save_dir.
    :rtype: None
    '''
    # General variables
    wait_time = 60 * 4
    save_dir = save_dir + '/' + query_word + '_videos'

    # Creating the save save_dir
    if not os.path.exists(save_dir):
        print("Save dir not found, creating save dir in:", save_dir)
        os.makedirs(save_dir)

    print(f"Downloading {max_n} videos of {args.query_word} videos!")
    search([query_word], save_dir, max_n, wait_time)


if __name__ == "__main__":
    # Defining the script's arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("query_word", type=str,
                        help="Search term to query in youtube (Only one search term at a time)")
    parser.add_argument("save_dir", type=str,
                        help="The path to the save_dir in which to save the downloads")
    parser.add_argument("-n", "number",
                        help="Max number of videos to download", default=1000)

    # Parsing arguments
    args = parser.parse_args()
    # Calling main function
    main(args.query_word, args.save_dir, args.number)
