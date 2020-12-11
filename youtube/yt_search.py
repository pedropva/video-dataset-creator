import subprocess as sp
import os
import youtube_dl
from multiprocessing import Pool
from time import sleep
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("query_word", type=str,
                    help="keyword to query")
parser.add_argument("path_to_save", type=str,
                    help="the absolute path to the save directory")
parser.add_argument("-n", "--number",
                    help="number of videos to download", default=1000)
args = parser.parse_args()


# https://www.reddit.com/r/learnpython/comments/3q1wfl/how_to_search_for_videos_in_youtubedl/
# you should be able to recover the video link by concatenating 'https://www.youtube.com/watch?v=' with the video id in the file name

donwloaded_count=0

wait_time = 60 * 4
save_dir = args.path_to_save+'/'+args.query_word+'_videos'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
amount = args.number # it can be a number or simply 'all'
print(f"Downloading {amount} videos of {args.query_word}")

def search(query):
    with youtube_dl.YoutubeDL(
        {
            "sleep_interval":wait_time,
            #"proxy":'207.91.10.234:8080',
            "quiet":False,
            "verbose":False,
            "no_warnings":True,
            "nooverwrites":True,
            "forceid":True,
            "ignoreerrors":True,
            #"dump_single_json": True,
            'format': 'best',
            "simulate": False,
            "default_search": f"ytsearch{amount}",
            'outtmpl': save_dir + '%(id)s.%(ext)s',
        }
    ) as ydl: 
        #result = ydl.extract_info(query,download=False) # uncomment this if we just want to extract the info
        ydl.download(query) #comment this if you dont want to download the video


out = search([args.query_word]) # query words can be a list too, such as ['boxing','MMA']