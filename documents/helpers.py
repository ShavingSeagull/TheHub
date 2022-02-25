# ------------------------------------
# Helper methods for the Documents app
# ------------------------------------

def tag_formatter(tag_list: list, extra_tags: str) -> str:
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

def tag_extractor(files: dict) -> list:
    """
    Takes a string of tags from the Google document/sheet
    metadata and extracts the tags into a list (per doc) for use
    on the frontend.
    """
    tags_per_file = []

    for file in files['files']:
        if "appProperties" in file:
            if "tags" in file['appProperties']:
                tags = file['appProperties']['tags']
                # Only splits up to three tags, as the frontend shouldn't display more than three
                tags_per_file.append({'id': file['id'], 'tags': tags.split(' ', 3)})
                if len(tags_per_file[-1]['tags']) > 3:
                    # While it will only split at three occurrences of a space, it will still
                    # add the remainder of the tags string to the new list. This will always
                    # be the final item of the list and thus can be removed safely with the
                    # -1 index. The list will never be longer than three items long.
                    last_appended_tags_list = tags_per_file[-1]['tags']
                    last_appended_tags_list.remove(last_appended_tags_list[-1])
    
    return tags_per_file
