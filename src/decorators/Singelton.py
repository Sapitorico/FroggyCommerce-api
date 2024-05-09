
def singelton(cls):
    """
    A decorator that converts a class into a singleton.

    Args:
        cls: The class to be converted into a singleton.

    Returns:
        The singleton instance of the class.
    """

    _instances = dict()

    def wrapper(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return wrapper
