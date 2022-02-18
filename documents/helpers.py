# ------------------------------------
# Helper methods for the Documents app
# ------------------------------------

def tag_list_formatter(tag_string: str):
    """
    Splits a string of tags into a list.
    Removes the whitespace from the list.
    """
    tag_list = tag_string.split(',')
    for x in range(len(tag_list)):
        tag_list[x] = tag_list[x].strip()

    return tag_list
