from crawlers.rnp.rnp_crawler import \
    log, \
    crawl_and_download, \
    scandown, \
    download_file, \
    sizeof_fmt

from crawlers.tests import utils
import os, pickle

test_save_dir = './tmp/'
CLIENT_KEY = 'YOUR KEY HERE'


def test_log():
    LOG_NAME = 'test_log.log'

    # Testing the log function without a output file (should just print)
    log('This is a logging test!', None)
    with open(LOG_NAME, 'w+') as log_file:
        log('This is a logging test!', log_file)
    with open(LOG_NAME, 'r') as log_file:
        assert log_file.read().strip() == 'This is a logging test!', 'Should be able to create and edit the log file.'

    # Cleaning log file
    os.remove(LOG_NAME)


def test_crawl_and_download():
    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    # Download some videos for testing purposes
    crawl_and_download(CLIENT_KEY, test_save_dir, max_n=2)

    # Checking if the videos were successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos=2)

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)


def test_scandown():
    with open('xml_sample.pickle', 'rb') as handle:
        test_nodes = pickle.load(handle)
    scandown(test_nodes)


def test_download_file():
    url = "http://video-rvd-maestro.rnp.br:80/vod/822/1440210731038.mp4"
    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    # Download a video for testing purposes
    assert download_file(url, test_save_dir) > 0, 'File size should be greater than zero.'

    # Checking if the video was successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos=1)

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)


def test_sizeof_fmt():
    assert sizeof_fmt(1024) == f'1.0 KiB', '1024 bytes should be 1.0 KiB.'
    assert sizeof_fmt(2048) == f'2.0 KiB', '2048 bytes should be 2.0 KiB.'
    assert sizeof_fmt(1024 * 1024) == f'1.0 MiB', '1024*1024 bytes should be 1.0 MiB.'
    assert sizeof_fmt(1024 ** 3) == f'1.0 GiB', '1024**3 bytes should be 1.0 GiB.'
