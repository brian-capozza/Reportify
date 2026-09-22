import os


def is_file_open(file_path: str):
    """checks if a file is open

    Args:
        file_path (str): The file path to the file to check

    Returns:
        bool: A true or false value corrresponding to whether or not the file is open
    """
    if not os.path.exists(file_path):
        return False  # File doesn't exist, so it's not open!

    try:
        # Try renaming the file to itself. If it's locked, Windows rejects this.
        os.rename(file_path, file_path)
        return False
    except OSError:
        return True