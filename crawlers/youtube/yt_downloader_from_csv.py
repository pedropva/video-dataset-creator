import subprocess as sp
import os
import youtube_dl
from multiprocessing import Pool
from time import sleep

saveDir = '/media/pedropva/proper_videos/yt_videos/'


#https://www.youtube.com/watch?v=sQ3aeclQ3QA                                                   
#/media/pedropva/datasets/yt_videos/sQ3aeclQ3QA.mp4
def already_downloaded(url):
    video_id = url.split('v=')[-1]
    video_path = saveDir + video_id
    if os.path.isfile(video_path+'.mp4') or os.path.isfile(video_path+'.webm'):
        return True
    else:
        #print(video_id,': ', url)
        return False

def download(url):
    try:
        options = {
            #'verbose': True,
            'format': 'best',
            'outtmpl': saveDir + '%(id)s.%(ext)s',
            #"source_address": "10.0.0.4",
            #'verbose':False,
            #'progress_hooks': [my_hook],
            #'noplaylist' : True,
            #'postprocessors': [{
            #    'key': 'FFmpegExtractAudio',
            #    'preferredcodec': 'mp3',
            #}],
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            #result = ydl.download([url])
            result = ydl.extract_info(url, download=True)#'https://www.youtube.com/watch?v=9bZkp7q19f0'
        
        filepath = saveDir + result['display_id']+'.'+result['ext']
        print('downloaded: ', filepath)
        return True
    except Exception as e: 
        print(e)
        return False

raw = open('valid_urls_2.csv').read().split('\n')
raw = [v for v in raw if v!='']
#raw = raw[:5500]

while(True):
    urls_to_download = []
    fails_sequence = 0 
    success_count = 0

    for url in raw:
        if already_downloaded(url):
            success_count += 1
        else:
            urls_to_download.append(url)

    print(f"{success_count} Videos already downloaded!")
    if len(urls_to_download) == 0:
        break
    #break
    # p = Pool(32)
    # p.starmap(download, zip(urls_to_download))


    for url in urls_to_download:
        print(url)
        result = download(url)
        if not result:
            print('### Failed downloading video! ###')
            fails_sequence +=1
        else:
            success_count += 1
            fails_sequence = 0

            wait_time = 30
            sleep(wait_time) # Time in seconds

        if(fails_sequence > 100):#if we failed more than 100 times, then just give up and try next time  
            break
    print(f'there were {success_count} out of {len(raw)} videos downloaded!')
    wait_time = 60 * 5
    sleep(wait_time) # Time in seconds