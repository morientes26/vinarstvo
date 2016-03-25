"""
Data utils
"""


def file_to_blob(input):
    """
    Read data from file and convert to array of byte
    Args:
        input: path to file

    Returns: byte[]

    """
    return open(input, "rb").read()

