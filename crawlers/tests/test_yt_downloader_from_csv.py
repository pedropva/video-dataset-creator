import os
from crawlers.youtube.yt_downloader_from_csv import \
    download,\
    already_downloaded,\
    read_csv_and_download_videos

from crawlers.tests import utils

test_save_dir = './tmp/'

def test_download():

    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    with open('./test_urls.csv','r') as csv_file:
        urls = csv_file.read().split('\n')

    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert download(url, test_save_dir), "Download should be sucessfull."

    utils.check_videos(test_save_dir, expected_number_of_videos = 3)

    utils.clean_temporary_dir(test_save_dir)

def test_already_downloaded():
    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    with open('./test_urls.csv', 'r') as csv_file:
        urls = csv_file.read().split('\n')

    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert download(url, test_save_dir), "Download should be sucessfull."

    utils.check_videos(test_save_dir, expected_number_of_videos=3)

    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert already_downloaded(url), "All videos should be already downloaded."

    utils.clean_temporary_dir(test_save_dir)

def test_read_csv_and_download_videos():
    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    with open('./test_urls.csv', 'r') as csv_file:
        urls = csv_file.read().split('\n')

    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert read_csv_and_download_videos(url, test_save_dir, wait_time=1), "Download should be sucessfull."

    utils.check_videos(test_save_dir, expected_number_of_videos=3)

    utils.clean_temporary_dir(test_save_dir)
