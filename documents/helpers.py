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

    Params
    ------
    tag_list: list
        A list of the tags retrieved from the frontend checkboxes

    extra_tags: str
        The string of all extra tags retrieved from the frontend input

    return type: str
    """
    formatted_extra_tags = ""

    for char in extra_tags:
        if char.isalnum() or char == ' ':
            formatted_extra_tags += char
    
    return f"{' '.join(tag_list)} {formatted_extra_tags}".strip()

def extra_tag_db_formatter(extra_tags: str) -> list:
    """
    Takes the string of extra tags and splits them into a list,
    stripping any whitespace from the start and end of each tag.
    Returns a list to be run through for the purpose of adding new
    tags to the database.

    Params
    ------
    extra_tags: str
        The string of extra tags to format

    return type: list
    """
    if extra_tags is None or extra_tags == '':
        return

    tag_holding_list = extra_tags.split(' ')
    tag_list = []

    # The list will contain an index with an empty element if the
    # user separates tags by more than one space on the frontend.
    # This removes those elements for the returned list.
    for x in range(len(tag_holding_list)):
        if tag_holding_list[x] != '':
            tag_list.append(tag_holding_list[x])

    for i in range(len(tag_list)):
        tag_list[i] = tag_list[i].strip()

    return tag_list

def tag_extractor(files: dict, for_frontend: bool = True) -> list:
    """
    Takes a string of tags from the Google document/sheet
    metadata and extracts the tags into a list (per doc).
    Can be used for frontend purposes (to show up to the
    limit of three tags on each doc) or to extract all tags
    for filtering and search purposes.

    Params
    ------
    files: dict
        The files retrieved from the Google Drive API call

    for_frontend: bool
        Whether the function is to extract only three tags
        to display for a doc overview (True/default), or
        whether it should extract all tags (False)

    return type: list
    """
    tags_per_file = []

    for file in files['files']:
        if "appProperties" in file:
            if "tags" in file['appProperties']:
                tags = file['appProperties']['tags']

                if for_frontend:
                    # Only splits up to three tags, as the frontend shouldn't display more than three
                    tags_per_file.append({'id': file['id'], 'tags': tags.split(' ', 3)})
                    if len(tags_per_file[-1]['tags']) > 3:
                        # While it will only split at three occurrences of a space, it will still
                        # add the remainder of the tags string to the new list. This will always
                        # be the final item of the list and thus can be removed safely with the
                        # -1 index. The list will never be longer than three items long.
                        last_appended_tags_list = tags_per_file[-1]['tags']
                        last_appended_tags_list.remove(last_appended_tags_list[-1])
                else:
                    # Splits every tag
                    tags_per_file.append({'id': file['id'], 'tags': tags.split(' ')})

    return tags_per_file

def user_creds_to_dict(user_creds_profile, scopes) -> dict:
    """
    Takes only the fields needed from the User's
    Google credentials profile in order to pass
    them to Google for authentication purposes.
    Cuts out things like the ID and the FK to the User.

    Params
    ------
    user_creds_profile: GoogleOauthCredentials object instance
        The instance of the user's Google auth creds

    return type: dict
    """
    user_creds = {
        'token': user_creds_profile.token,
        'refresh_token': user_creds_profile.refresh_token,
        'token_uri': user_creds_profile.token_uri,
        'client_id': user_creds_profile.client_id,
        'client_secret': user_creds_profile.client_secret,
        'scopes': scopes
    }

    return user_creds
