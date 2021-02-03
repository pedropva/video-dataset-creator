import os
from glob import glob
import os


def create_dir(test_save_dir: str):
    """Creates a temporary directory for automated testing.

     :param test_save_dir: Name of directory to be created.
     :type string: str, optional

     :returns: None
     """
    # Creating the save save_dir
    if not os.path.exists(test_save_dir):
        os.makedirs(test_save_dir)


def check_videos(test_save_dir, expected_number_of_videos):
    """Checks for the existence and size of video files in order to confirm that they were successfully downloaded.

     :param test_save_dir: Path to the directory containing the videos.
     :param expected_number_of_videos: The expected number of videos in the folder.
     :returns: None
    """
    # Look for the files in the tmp folder
    exts = ['*.mp4', '*.webm']
    temp_files = [f for ext in exts for f in glob(os.path.join(test_save_dir, ext))]

    # Test if videos exist
    assert len(
        temp_files) == expected_number_of_videos, f'Failed to search and download test videos. Expected {expected_number_of_videos}, got {len(temp_files)}.'

    # Checking if the videos were completely downloaded (their size has to be different than 0)
    for fpath in temp_files:
        assert os.path.isfile(fpath) and os.path.getsize(fpath) > 0, 'Failed to complete download of test videos.'


def clean_temporary_dir(test_save_dir):
    """Removes all files inside the temporary dir. Then it removes the temporary directory itself.

     :param test_save_dir: Path to the temporary directory.
     :returns: None
    """
    # Cleaning the temporary test dir
    temp_files = glob(test_save_dir + '*')
    for fpath in temp_files:
        print(f'Removing file {fpath}')
        os.remove(fpath)

    # Deleting the temporary dir
    if os.path.exists(test_save_dir):
        print(f'Removing temporary dir {test_save_dir}')
        os.rmdir(test_save_dir)
