def format_datetime(datetime_obj):
    """
    Formats a datetime object into a string representation.
    """
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S') if datetime_obj else None
