# ------------------------------------
# Helper methods for the Documents app
# ------------------------------------

def tags_formatter(tag_list: list, extra_tags: str) -> str:
    """
    Google Drive API only allows strings as custom metadata.
    This takes the list of checkbox tags and the string of extra
    tags and combines them into one, space-separated, string.
    The original set of extra tags, which come as one string,
    are checked and built into a new string, in order to remove
    any rogue punctuation the user may have entered. Numbers that
    are part of the tag name and the spaces between them are preserved.
    """
    formatted_extra_tags = ""

    for char in extra_tags:
        if char.isalnum() or char == ' ':
            formatted_extra_tags += char
    
    return f"{' '.join(tag_list)} {formatted_extra_tags}".strip()
