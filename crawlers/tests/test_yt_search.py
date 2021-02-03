from crawlers.youtube.yt_search import search
from crawlers.tests import utils

from glob import glob
import os

def test_search():
    test_query = ['sudoku']
    test_save_dir = './tmp/'

    # Creating the save save_dir
    utils.create_dir(test_save_dir)

    #Download some videos for testing purposes
    search(test_query, test_save_dir, max_n = 2, wait_time = 0)

    # Checking if the videos were successfully downloaded
    utils.check_videos(test_save_dir, expected_number_of_videos = 2)

    # Clean up test files
    utils.clean_temporary_dir(test_save_dir)