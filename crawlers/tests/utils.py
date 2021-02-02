import os
from glob import glob
import os

def create_dir(test_save_dir):
    # Creating the save save_dir
    if not os.path.exists(test_save_dir):
        os.makedirs(test_save_dir)

def check_videos(test_save_dir, expected_number_of_videos):

    # Look for the files in the tmp folder
    exts = ['*.mp4', '*.webm']
    temp_files = [f for ext in exts for f in glob(os.path.join(test_save_dir, ext))]

    # Test if videos exist
    assert len(temp_files) == expected_number_of_videos, 'Failed to search and download test videos.'

    # Checking if the videos were completely downloaded (their size has to be different than 0)
    for fpath in temp_files:
        assert os.path.isfile(fpath) and os.path.getsize(fpath) > 0, 'Failed to complete download of test videos.'

def clean_temporary_dir(test_save_dir):
    # Cleaning the temporary test dir
    temp_files = glob(test_save_dir + '*')
    for fpath in temp_files:
        print(f'Removing file {fpath}')
        os.remove(fpath)

    # Deleting the temporary dir
    if os.path.exists(test_save_dir):
        print(f'Removing temporary dir {test_save_dir}')
        os.rmdir(test_save_dir)