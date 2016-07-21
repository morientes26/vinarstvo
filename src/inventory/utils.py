"""
Data and render utils
"""
import inventory

def file_to_blob(input):
    """
    Read data from file and convert to array of byte
    Args:
        input: path to file

    Returns: byte[]

    """
    return open(input, "rb").read()


def default_controller_values(request):
    """
    Context processor for default values of controller.
    Args:
        request:

    Returns:

    """
    return {'app_version': inventory.__version__}
