import os
from crawlers.youtube.yt_downloader_from_csv import \
    download,\
    already_downloaded,\
    read_csv_and_download_videos

from crawlers.tests import utils

test_save_dir = './tmp/'
test_csv_path = './test_urls.csv'

def test_download():

    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    # Load the urls csv
    with open(test_csv_path,'r') as csv_file:
        urls = csv_file.read().split('\n')

    # Download each video from the urls
    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert download(url, test_save_dir), "Download should be sucessfull."

    # Checking if the videos were successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos = 3)

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)

def test_already_downloaded():
    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    # Load the urls csv
    with open(test_csv_path, 'r') as csv_file:
        urls = csv_file.read().split('\n')

    # Download each video from the urls
    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert download(url, test_save_dir), "Download should be sucessfull."

    # Checking if the videos were successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos=3)

    # Knowing that the videos were successfully downloaded, test if the already downloaded funcion really works
    for url in urls:
        if url != '':
            url = url.replace(',', '')
            assert already_downloaded(url, test_save_dir), "All videos should be already downloaded."

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)

def test_read_csv_and_download_videos():

    # Testing the full pipeline
    read_csv_and_download_videos(test_csv_path, test_save_dir, wait_time=1)

    # Checking if the videos were successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos=3)

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)

